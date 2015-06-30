"use strict";

module.exports = function(grunt) {

    grunt.loadNpmTasks("grunt-bower-install-simple");
    grunt.loadNpmTasks("grunt-contrib-concat");
    grunt.loadNpmTasks("grunt-contrib-copy");
    grunt.loadNpmTasks("grunt-contrib-less");
    grunt.loadNpmTasks("grunt-contrib-watch");
    grunt.loadNpmTasks('grunt-exec');



    grunt.initConfig({

        /*
        exec: {
            loadblogposts: {
                command:'python manage.py loadblogposts'
            },
            loadtopofpagecontent: {
                command:'python manage.py loadtopofpagecontent'
            },
            loadcalendarevents: {
                command:'python manage.py loadcalendarevents'
            },
            loadnewsarticles: {
                command:'python manage.py loadnewsarticles'
            },
            loadfounderpublications: {
                command:'python manage.py loadfounderpublications'
            },
        },
        */


        watch: {
          lessfiles: {
            files: ['app/static/source/less/**/*.less'],
            tasks: ['less'],
            options: {
              spawn: true,
            },
          },



        },

        less: {
            common_css: {
                options: {
                  compress: false,
                  yuicompress: false,
                },
                files: {
                  "app/static/source/css/main.css": "app/static/source/less/main.less" // destination file and source file
                }
            },
            index_css: {
                options: {
                  compress: false,
                  yuicompress: false,
                  /*optimization: 2*/
                },
                files: {
                  "app/static/source/css/views/index.css": "app/static/source/less/views/index.less" // destination file and source file
                }
            },
            editPlate_css: {
                options: {
                  compress: false,
                  yuicompress: false,
                  /*optimization: 2*/
                },
                files: {
                  "app/static/source/css/views/editPlate.css": "app/static/source/less/views/editPlate.less" // destination file and source file
                }
            },
            sampleReport_css: {
                options: {
                  compress: false,
                  yuicompress: false,
                  /*optimization: 2*/
                },
                files: {
                  "app/static/source/css/views/sampleReport.css": "app/static/source/less/views/sampleReport.less" // destination file and source file
                }
            },
            plateReport_css: {
                options: {
                  compress: false,
                  yuicompress: false,
                  /*optimization: 2*/
                },
                files: {
                  "app/static/source/css/views/plateReport.css": "app/static/source/less/views/plateReport.less" // destination file and source file
                }
            },
            index_ie8_css: {
                options: {
                  compress: false,
                  yuicompress: false,
                  /*optimization: 2*/
                },
                files: {
                  "app/static/source/css/views/index_ie8.css": "app/static/source/less/views/index_ie8.less" // destination file and source file
                }
            },
            index_ie9_css: {
                options: {
                  compress: false,
                  yuicompress: false,
                  /*optimization: 2*/
                },
                files: {
                  "app/static/source/css/views/index_ie9.css": "app/static/source/less/views/index_ie9.less" // destination file and source file
                }
            },
        },

        copy: {

            bootstrapTypeahead_js: {
                cwd: 'app/static/bower_components/bs-typeahead/js',
                src: '**/bootstrap-typeahead.min.js',
                dest: 'app/static/js',
                expand: true
            },

            easyModal_js: {
                cwd: 'app/static/bower_components/easyModal.js',
                src: '**/jquery.easyModal.js',
                dest: 'app/static/js',
                expand: true
            },

            handlebars_js: {
                cwd: 'app/static/bower_components/handlebars',
                src: '**/handlebars.min.js',
                dest: 'app/static/js',
                expand: true
            },

            moment_js: {
                cwd: 'app/static/bower_components/moment/min',
                src: '**/*.js',
                dest: 'app/static/js',
                expand: true
            },

            rlite_js: {
                cwd: 'app/static/bower_components/rlite',
                src: '**/*.js',
                dest: 'app/static/js',
                expand: true
            },

            jquery_js: {
                cwd: 'app/static/bower_components/jquery/dist',
                src: '**/*',
                dest: 'app/static/js',
                expand: true
            },

            jquery_easing_js: {
                cwd: 'app/static/bower_components/jquery.easing/js',
                src: '**/*.js',
                dest: 'app/static/js',
                expand: true
            },

            underscore_js: {
                cwd: 'app/static/bower_components/underscore',
                src: ['underscore*.js'],
                dest: 'app/static/js',
                expand: true
            },

            bootstrap_js: {
                cwd: 'app/static/bower_components/bootstrap/dist/js',
                src: '**/*',
                dest: 'app/static/js',
                expand: true
            },

            bootstrap_css: {
                cwd: 'app/static/bower_components/bootstrap/dist/css',
                src: '**/*',
                dest: 'app/static/css',
                expand: true
            },

            bootstrap_fonts: {
                cwd: 'app/static/bower_components/bootstrap/dist/fonts',
                src: '**/*',
                dest: 'app/static/fonts',
                expand: true
            },

            fontawesome_css: {
                cwd: 'app/static/bower_components/font-awesome/css',
                src: '**/*',
                dest: 'app/static/css',
                expand: true
            },

            fontawesome_fonts: {
                cwd: 'app/static/bower_components/font-awesome/fonts',
                src: '**/*',
                dest: 'app/static/fonts',
                expand: true
            },


            remodal_js: {
                cwd: 'app/static/bower_components/remodal/dist',
                src: '**/*.js',
                dest: 'app/static/js',
                expand: true
            },

            remodal_css: {
                cwd: 'app/static/bower_components/remodal/dist',
                src: '**/*.css',
                dest: 'app/static/css',
                expand: true
            },

            source_images: {
                cwd: 'app/static/source/images',
                src: '**/*',
                dest: 'app/static/images',
                expand: true
            },



        },

        concat: {
            jquery: {
                files: {


                    //
                    // Bootstrap - Fonts
                    //
                    'app/static/fonts/glyphicons-halflings-regular.eot': ['app/static/bower_components/bootstrap/dist/fonts/glyphicons-halflings-regular.eot'],
                    'app/static/fonts/glyphicons-halflings-regular.svg': ['app/static/bower_components/bootstrap/dist/fonts/glyphicons-halflings-regular.svg'],
                    'app/static/fonts/glyphicons-halflings-regular.ttf': ['app/static/bower_components/bootstrap/dist/fonts/glyphicons-halflings-regular.ttf'],
                    'app/static/fonts/glyphicons-halflings-regular.woff': ['app/static/bower_components/bootstrap/dist/fonts/glyphicons-halflings-regular.woff'],
                    'app/static/fonts/glyphicons-halflings-regular.woff2': ['app/static/bower_components/bootstrap/dist/fonts/glyphicons-halflings-regular.woff2'],


                }
            }
        },
        "bower-install-simple": {
            options: {
                color: true,
                /*directory: "app/components"*/
            },
            "prod": {
                options: {
                    production: true
                }
            },
            "dev": {
                options: {
                    production: false
                }
            }
        }
    });

    grunt.event.on('watch', function(action, filepath, target) {
       grunt.log.writeln(target + ': ' + filepath + ' has ' + action);
    });

   // grunt.registerTask('watch', 'Running "DEFAULT", compiling everything.', [
   //     'watch:lessfiles'
   // ]);


    grunt.registerTask('default', 'Running "DEFAULT", compiling everything.', [
        'bower-install-simple',
        'less:common_css',
        'less:index_css',
        'less:index_ie8_css',
        'less:index_ie9_css',


        'copy:bootstrapTypeahead_js',
        'copy:easyModal_js',
        'copy:handlebars_js',

        'copy:rlite_js',
        'copy:moment_js',
        'copy:jquery_js',
        'copy:jquery_easing_js',
        'copy:underscore_js',
        'copy:bootstrap_js',
        'copy:bootstrap_css',
        'copy:bootstrap_fonts',
        'copy:fontawesome_css',
        'copy:fontawesome_fonts',
        'copy:source_images',
    ]);

    grunt.registerTask('heroku', 'Running "DEFAULT", compiling everything.', [
        'bower-install-simple',
        'less:common_css',
        'less:index_css',
        'less:index_ie8_css',
        'less:index_ie9_css',

        'copy:bootstrapTypeahead_js',
        'copy:easyModal_js',
        'copy:handlebars_js',

        'copy:rlite_js',
        'copy:moment_js',
        'copy:jquery_js',
        'copy:jquery_easing_js',
        'copy:underscore_js',
        'copy:bootstrap_js',
        'copy:bootstrap_css',
        'copy:bootstrap_fonts',
        'copy:fontawesome_css',
        'copy:fontawesome_fonts',
        'copy:source_images',
    ]);


};