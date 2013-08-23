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
        min:{
            base:{
                src:[jsStaticFolder + 'base.js',
                    jsStaticFolder + 'help.js'],
                dest:jsStaticFolder + 'base.min.js'
            },
            details:{
                src:[jsStaticFolder + 'details.js',
                    jsStaticFolder + 'libs/XMLDisplay.js'],
                dest:jsStaticFolder + 'details.min.js'
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
                src:[jsStaticFolder + 'libs/flexigrid.js',
                    jsStaticFolder + 'libs/bootstrap-contextmenu.js'],
                dest:jsStaticFolder + 'libs/flexigrid.min.js'
            },
            accessibility:{
                src:[jsStaticFolder + 'accessibility.js'],
                dest:jsStaticFolder + 'accessibility.min.js'
            },
        }
    });
};
