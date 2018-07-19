/**
 *	Gruntfile
 *	@author Una Ada (Trewbot) <una@phene.co>
 *	2016.12.10
 */

module.exports = function(grunt){
	grunt.initConfig({
		pkg : grunt.file.readJSON('package.json'),
		sass : {
			dist : {
				options : {
					outputStyle	: 'compressed'
				},
				files : [{
					expand	: true,
					cwd		: 'styles/',
					src		: ['*.scss'],
					dest	: 'client/assets/style',
					ext		: '.css'
				}]
			}
		},
		autoprefixer : {
			compile : {
				files : {
					'client/assets/style/main.css': 'client/assets/style/main.css'
				}
			}
		},
        pug: {
            compile: {
                files: [{
                    expand  : true,
                    cwd     : 'client/',
                    src     : ['*.pug'],
                    dest    : 'client/',
                    ext     : '.html'
                }]
            }
        },
		watch : {
			sass : {
				files : ['styles/*.scss'],
				tasks : ['sass','autoprefixer']
			},
            pug : {
                files : ['client/*.pug'],
                tasks : ['pug']
            }
		}
	});
	grunt.loadNpmTasks('grunt-sass');
    grunt.loadNpmTasks('grunt-autoprefixer');
	grunt.loadNpmTasks('grunt-contrib-pug');
	grunt.loadNpmTasks('grunt-contrib-watch');
};
