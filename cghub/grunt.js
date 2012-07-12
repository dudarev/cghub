module.exports = function (grunt) {
    "use strict";
    var staticFolder = 'static/',
        cssStaticFolder = staticFolder + 'css/',
        jsStaticFolder = staticFolder + 'js/';
    grunt.loadNpmTasks('grunt-less');
    grunt.initConfig({
        less:{
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
            core_home:{
                src:cssStaticFolder + 'core/home.less',
                dest:cssStaticFolder + 'core/home.css',
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
            }
        },
        min:{
            base:{
                src:[jsStaticFolder + 'base.js'],
                dest:jsStaticFolder + 'base.min.js'
            },
            bootstrap:{
                src:[jsStaticFolder + 'libs/bootstrap/dev/*.js'],
                dest:jsStaticFolder + 'libs/bootstrap/bootstrap.min.js'
            },
            cart:{
                src:[jsStaticFolder + 'cart/cart.js'],
                dest:jsStaticFolder + 'cart/cart.min.js'
            },
            core_home:{
                src:[jsStaticFolder + 'core/home.js'],
                dest:jsStaticFolder + 'core/home.min.js'
            },
            core_search:{
                src:[jsStaticFolder + 'core/search.js'],
                dest:jsStaticFolder + 'core/search.min.js'
            }
        }
    });
};
