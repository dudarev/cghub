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
        }
    });
};
