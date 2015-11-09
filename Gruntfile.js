"use strict";

module.exports = function(grunt) {

    grunt.loadNpmTasks("grunt-bower-install-simple");
    grunt.loadNpmTasks("grunt-contrib-concat");
    grunt.loadNpmTasks("grunt-contrib-copy");
    grunt.loadNpmTasks("grunt-contrib-less");
    grunt.loadNpmTasks("grunt-contrib-watch");
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-jade');
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-githash');
    grunt.loadNpmTasks('grunt-exec');
    grunt.loadNpmTasks('grunt-html2js');

    grunt.initConfig({

        // NEW ANGULAR APP

        githash: {
            main: {
              options: {},
            }
        }

        ,watch: {
            javascript: {
                files: 'app/static/source/js/**/*.js'
                ,tasks: ['githash', 'clean:twist_app_js', 'uglify:twist_app']
            }
            ,stylesheets: {
                files: 'app/static/source/scss/**/*.scss'
                ,tasks: ['githash', 'clean:twist_app_css', 'sass:all']
            }
            ,index_template: {
                files: 'app/static/source/jade/index.jade'
                ,tasks: ['githash', 'jade:compile_home']
            }
            ,other_templates: {
                files: 'app/static/source/jade/other_templates/**/*.jade'
                ,tasks: ['clean:compiled_templates', 'jade:compile_templates', 'html2js']
            }
            ,images: {
                files: 'app/static/source/images/**/*'
                ,tasks: ['copy:source_images']
            }
        }

        ,uglify: {
            twist_app: {
                files: {
                    'app/static/js/twist-app<%= githash.main.short %>.js': [
                        'app/static/source/js/*.js'
                    ]
                }
            }
        }

        ,sass: {
            all: {
                files: {
                    'app/static/css/twist-app<%= githash.main.short %>.css': 'app/static/source/scss/**/*.scss'
                }
            }
        }

        ,jade: {
            compile_home: {
                options: {
                    pretty: true
                    ,doctype: 'html'
                    ,data: {
                        'githash': '<%= githash.main.short %>'
                        ,'app_domain_name': grunt.option('app_domain_name')
                    }
                }
                ,files: {
                  "app/static/index.html": ["app/static/source/jade/index.jade"]
                }
            }
            ,compile_templates: {
                options: {
                    pretty: true
                    ,doctype: 'html'
                }
                ,files: [
                    {
                        cwd: "app/static/source/jade/other_templates"
                        ,src: "**/*.jade"
                        ,dest: "app/static/source/jade/compiled_templates"
                        ,expand: true
                        ,ext: ".html"
                    }
                ]
            }
        }

        ,html2js: {
            options: {
                base: 'app/static/source/jade/compiled_templates'
            },
            main: {
                src: ['app/static/source/jade/compiled_templates/**/*.html']
                ,dest: 'app/static/source/js/templates.js'
            },
        }

        ,clean: {
            twist_app_js: [
                'app/static/js/twist-app*.js'
            ],
            twist_app_css: [
                'app/static/css/twist-app*.css'
            ],
            compiled_templates: [
                'app/static/source/jade/compiled_html'
                ,'app/static/source/js/templates.js'
            ]
        }

        //END NEW ANGULAR APP

        ,less: {
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
            recordSampleTransfer_css: {
                options: {
                  compress: false,
                  yuicompress: false,
                  /*optimization: 2*/
                },
                files: {
                  "app/static/source/css/views/recordSampleTransfer.css": "app/static/source/less/views/recordSampleTransfer.less" // destination file and source file
                }
            },

            viewSampleTransfers_css: {
                options: {
                  compress: false,
                  yuicompress: false,
                  /*optimization: 2*/
                },
                files: {
                  "app/static/source/css/views/viewSampleTransfers.css": "app/static/source/less/views/viewSampleTransfers.less" // destination file and source file
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



            // NEW ANGULAR APP
            twist_app_index: {
                src: 'app/static/source/jade/compiled_html/index.html'
                ,dest: 'app/static/index.html'
            }
            ,twist_app_other_js: {
                cwd: 'app/static/bower_components'
                ,src: [
                    'jquery/dist/jquery.min.js'
                    ,'jquery/dist/jquery.min.map'
                    ,'angular/angular.js'
                    ,'angular/angular.min.js'
                    ,'angular/angular.min.js.map'
                    ,'angular-ui-router/release/angular-ui-router.*'
                    ,'angular-bootstrap/ui-bootstrap.min.js'
                    ,'angular-bootstrap/ui-bootstrap-tpls.min.js'
                    ,'angular-sanitize/angular-sanitize.min.js'
                    ,'angular-sanitize/angular-sanitize.min.js.map'
                    ,'js-xlsx/dist/xlsx.full.min.js'
                    ,'js-xlsx/dist/xlsx.full.min.map'
                    ,'file-saver/FileSaver.min.js'
                    ,'angular-local-storage/dist/angular-local-storage.min.js'
                ]
                ,dest: 'app/static/js'
                ,flatten: true
                ,expand: true
            }

            ,twist_app_other_css: {
                cwd: 'app/static/bower_components'
                ,src: [
                    'bootstrap/dist/css/bootstrap.min.css'
                    ,'bootstrap/dist/css/bootstrap.css.map'
                ]
                ,dest: 'app/static/css'
                ,flatten: true
                ,expand: true
            }

            // END NEW ANGULAR APP



            ,bootstrapTypeahead_js: {
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
        'copy:jquery_easing_js',
        'copy:underscore_js',
        'copy:bootstrap_js',
        'copy:bootstrap_css',
        'copy:bootstrap_fonts',
        'copy:fontawesome_css',
        'copy:fontawesome_fonts',
        'copy:source_images',


        // NEW ANGULAR APP
        'githash'
        ,'clean'
        ,'jade:compile_home'
        ,'jade:compile_templates'
        ,'html2js'
        ,'uglify:twist_app'
        ,'sass:all'
        ,'copy:twist_app_index'
        ,'copy:twist_app_other_js'
        ,'copy:twist_app_other_css'
        //END NEW ANGULAR APP
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


        // NEW ANGULAR APP
        'githash'
        ,'clean'
        ,'jade:compile_home'
        ,'jade:compile_templates'
        ,'html2js'
        ,'uglify:twist_app'
        ,'sass:all'
        ,'copy:twist_app_index'
        ,'copy:twist_app_other_js'
        ,'copy:twist_app_other_css'
        //END NEW ANGULAR APP
    ]);

};