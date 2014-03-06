"use strict";

module.exports = function (grunt) {
    var staticFolder = 'static/',
        cssStaticFolder = staticFolder + 'css/',
        jsStaticFolder = staticFolder + 'js/';

    grunt.loadNpmTasks('grunt-recess');
    grunt.loadNpmTasks('grunt-contrib-uglify');

    grunt.initConfig({
        recess:{
            bootstrap:{
                src:cssStaticFolder + 'libs/bootstrap/less/bootstrap.less',
                dest:cssStaticFolder + 'libs/bootstrap/bootstrap.css',
                options:{
                    compress:true
                }
            },
            cart:{
                src:cssStaticFolder + 'cart/cart.less',
                dest:cssStaticFolder + 'cart/cart.css',
                options:{
                    compress:true
                }
            },
            core_help:{
                src:cssStaticFolder + 'core/help.less',
                dest:cssStaticFolder + 'core/help.css',
                options:{
                    compress:true
                }
            },
            core_search:{
                src:cssStaticFolder + 'core/search.less',
                dest:cssStaticFolder + 'core/search.css',
                options:{
                    compress:true
                }
            },
            core_batch_search:{
                src:cssStaticFolder + 'core/batch_search.less',
                dest:cssStaticFolder + 'core/batch_search.css',
                options:{
                    compress:true
                }
            },
            core_details:{
                src:cssStaticFolder + 'core/details.less',
                dest:cssStaticFolder + 'core/details.css',
                options:{
                    compress:true
                }
            },
            core_error: {
                src:cssStaticFolder + 'core/error.less',
                dest:cssStaticFolder + 'core/error.css',
                options:{
                    compress:true
                }
            },
            flexigrid:{
                src:cssStaticFolder + 'libs/flexigrid/flexigrid.css',
                dest:cssStaticFolder + 'libs/flexigrid/flexigrid.min.css',
                options:{
                    compress:true
                }
            }
        },
        uglify:{
            base:{
                src:[jsStaticFolder + 'base.js',
                    jsStaticFolder + 'help.js'],
                dest:jsStaticFolder + 'base.min.js'
            },
            jquery_libs:{
                src:[jsStaticFolder + 'libs/jquery-1.7.2.min.js',
                    jsStaticFolder + 'libs/jquery-ui-1.8.20.custom.min.js',
                    jsStaticFolder + 'libs/jquery.cookie.min.js',
                    jsStaticFolder + 'libs/URI.min.js',
                    jsStaticFolder + 'libs/ui.dropdownchecklist.js',
                    jsStaticFolder + 'libs/jquery.placeholder.min.js'],
                dest:jsStaticFolder + 'jquery.libs.min.js'
            },
            xmldisplay:{
                src:[jsStaticFolder + 'libs/XMLDisplay.js'],
                dest:jsStaticFolder + 'libs/XMLDisplay.min.js'
            },
            cart:{
                src:[jsStaticFolder + 'cart/cart.js',
                    jsStaticFolder + 'table.js'],
                dest:jsStaticFolder + 'cart/cart.min.js'
            },
            core_home:{
                src:[jsStaticFolder + 'core/home.js'],
                dest:jsStaticFolder + 'core/home.min.js'
            },
            core_search:{
                src:[jsStaticFolder + 'core/search.js',
                    jsStaticFolder + 'table.js'],
                dest:jsStaticFolder + 'core/search.min.js'
            },
            core_batch_search:{
                src:[jsStaticFolder + 'core/batch_search.js',
                    jsStaticFolder + 'table.js'],
                dest:jsStaticFolder + 'core/batch_search.min.js'
            },
            flexigrid:{
                src:[jsStaticFolder + 'libs/flexigrid.js'],
                dest:jsStaticFolder + 'libs/flexigrid.min.js'
            },
            accessibility:{
                src:[jsStaticFolder + 'accessibility.js'],
                dest:jsStaticFolder + 'accessibility.min.js'
            }
        }
    });
};
