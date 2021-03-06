######################################################################################
#
# Copyright (c) 2015 Twist Bioscience
#
# File: app/routes/authentication.py
#
# These are the handlers for all authentication-related routes in this application.
#
######################################################################################

from flask import g, render_template, request, redirect, url_for, abort

from app import app, db

from twistdb.public import Operator
from app import login_manager

import requests

from app import googlelogin

from flask_login import login_user, logout_user, current_user

from logging_wrapper import get_logger
logger = get_logger(__name__)

######################################################################################
#
# "Authentication" Helper Methods
#
######################################################################################


@app.before_request
def before_request():
    app.config['GOOGLE_LOGIN_REDIRECT_URI'] = \
        url_for('oauth2callback', _external=True)
    g.user = current_user


def login_to_google(code, redirect_uri):

    token = requests.post(app.config['GOOGLE_OAUTH2_TOKEN_URL'], data=dict(
        code=code,
        redirect_uri=redirect_uri,
        grant_type='authorization_code',
        client_id=app.config['GOOGLE_LOGIN_CLIENT_ID'],
        client_secret=app.config['GOOGLE_LOGIN_CLIENT_SECRET'],
    )).json
    logger.info('@@ token: %s' % token)

    if not token or token.get('error'):
        logger.error("Error requesting auth token from Google")
        abort(400)

    userinfo = requests.get(app.config['GOOGLE_OAUTH2_USERINFO_URL'], params=dict(
        access_token=token['access_token'],
    )).json
    if not userinfo or userinfo.get('error'):
        logger.error("Error requesting user info from Google")
        abort(400)

    return token, userinfo


@login_manager.user_loader
def load_user(operator_id):
    """
    Magically called by google_login plumbing when "login_user" is invoked
    (see "create_or_update_user").
    """
    # FIXME: this function used to expect email address, but actually recieved the intials / operator_id
    #   (which seem to be the same thing, and what's returned by __unicode__)
    return db.session.query(Operator).filter_by(operator_id=operator_id).one()


def create_or_update_user(token, userinfo, **params):
    """
    Called by the "oauth2callback" route code once the user's token and info
    have been retrieved. It is within this code that we look up the user in
    the "Operator" table and assign that user to the google_login "current_user"
    object and the g.user object.
    """

    user_email = userinfo.get("email")

    logger.info(" Login attempt for user with email [%s]" % (user_email))
    operator = db.session.query(Operator).filter_by(email=user_email).first()

    if operator:
        logger.info(" User [%s - %s] logged in. Hello!" % (operator.first_and_last_name, operator.email))
    else:
        logger.error("Login attempt for user with email [%s] but user not in operator table" % (user_email))
        return redirect(url_for('user_missing_from_operator_table'))

    #
    # This causes the "load_user" function to be called!!!
    #
    if login_user(operator):
        g.user = operator

    return redirect(url_for('new_home'))


# ==========================
#
# "Authentication" Route Handlers
#
# ==========================


def login():
    """Show the "login" page (the one with a Google "Sign In" button)."""
    return render_template(
        'login.html', login_url=googlelogin.login_url(
            scopes=['https://www.googleapis.com/auth/userinfo.email']))


def user_missing_from_operator_table():
    """
    The user logged in via their Gmail account,
    but they aren't in the "operator" table.
    """
    return render_template('user_missing_from_operator_table.html',
                           login_url=url_for('new_home'))


def oauth2callback():
    """
    This is invoked when the user clicks the "Sign In" button and enters their
    Google login (email+password). Google oauth calls this function - passing
    in (via URL query parameter) a "code" value if the user clicked the
    Accept/Allow button when first logging in. If the user clicked
    Cancel/Decline instead, then no code value will be returned.
    """
    #
    # If there is a "code" value, then that means the user successfully
    # logged in. At this point, we'll make a call to google - exchanging that
    # code value for a token and user data.
    #
    code = request.args.get('code')

    if code:
        token, userinfo = login_to_google(
            code, url_for('oauth2callback', _external=True))
        return create_or_update_user(token, userinfo)

    #
    # If the user gets to the point of logging in to google but then declines to allow our app
    # to access their credentials, "code" will not be sent to us. In that case, we just redirect back
    # to our login page again.
    #
    else:
        return redirect(url_for('new_home'))


def logout():
    """
    This is a "GET" route that logs the user out from Google oauth
    (and from this application)
    """
    if g.user:
        logger.info(" User [%s - %s] logged out. Bye!" %
                    (g.user.first_and_last_name, g.user.email))

    logout_user()
    g.user = None
    return redirect(url_for('new_home'))
