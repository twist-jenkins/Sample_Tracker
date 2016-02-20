const exec = require('child_process').exec;
const gulp = require('gulp');
const gutil = require('gulp-util');
const rm = require('gulp-rimraf');
const shell = require('gulp-shell')
const webpack = require('webpack');
//const KarmaServer = require('karma').Server;
const WebpackDevServer = require('webpack-dev-server');

////////////////////////////////////////////////////////////////////////////////

const FLASK_CMD = 'export PYTHONUNBUFFERED=1; source venv/bin/activate && python manage.py runserver'
const FLASK_URL = 'http://localhost:5000'
const UI_DIR = 'app/ui';
const UI_HOST = 'localhost'
const UI_PORT = 9001
const UI_URL = 'http://' + UI_HOST + ':' + UI_PORT
const WEBPACK_CONFIG_FILE = require('./' + UI_DIR + '/webpack.config.js');

////////////////////////////////////////////////////////////////////////////////

// start Flask server
gulp.task('flask', function(done) {
	// allow overriding FLASK_CMD with `gulp dev --py "SHELL COMMAND HERE"`
	const cmd = (!gutil.env.py ? FLASK_CMD : gutil.env.py)

	gutil.log('[flask-command]', cmd)
	gutil.log('[flask-server]', FLASK_URL);

	// execute FLASK_CMD processes and forward their output to stderr and stdout
	var proc = exec(cmd);
	proc.stderr.on('data', function(data){
		process.stderr.write('[flask] ' + data);
	});
	proc.stdout.on('data', function(data){
		process.stdout.write('[flask] ' + data);
	});
});

// open web browser to FLASK_URL
gulp.task('open-browser', function(done) {
	exec('open ' + FLASK_URL);
});

gulp.task('webpack-dev', function(done) {
	var myConfig = Object.create(WEBPACK_CONFIG_FILE);
	myConfig.devtool = 'eval';
	myConfig.debug = true;

	new WebpackDevServer(webpack(myConfig), {
		contentBase: UI_DIR,
		stats: {colors: true}
	}).listen(UI_PORT, UI_HOST, function(err) {
		if (err) throw new gutil.PluginError('webpack-dev-server', err);
		gutil.log('[webpack-dev-server]', UI_URL);
	});
	done();
});

//gulp.task('karma', function(done) {
//  var server = new KarmaServer({
//	  configFile: UI_DIR + '/test/karma.conf.js',
//	  singleRun: false
//  }, done);
//  server.start();
//});
//
//gulp.task('karma:ci', function(done) {
//	var server = new KarmaServer({
//  	  configFile: UI_DIR + '/test/karma.ci.conf.js',
//  	  singleRun: true
//    }, done);
//    server.start();
//});

gulp.task('clean', function() {
    return gulp.src(UI_DIR + '/dist/*').pipe(rm());
});

gulp.task('package', ['clean'], function(done) {
	var myConfig = Object.create(WEBPACK_CONFIG_FILE);
	myConfig.devtool = 'eval';
	myConfig.debug = true;

	webpack(myConfig, function(err, stats) {
		if (stats.compilation.errors.length) {
			throw new gutil.PluginError('webpack', stats.compilation.errors.toString());
		}
		if (stats.compilation.warnings.length) {
			gutil.log('[WARNING]', stats.compilation.warnings.toString())
		}
		done();
	});
});

////////////////////////////////////////////////////////////////////////////////

gulp.task('build', ['package']);

gulp.task('dev', ['webpack-dev', 'flask', 'open-browser']);

gulp.task('default', ['dev']);
