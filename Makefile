# constants
#

-include Makefile.def

#
# end of constants

# targets
#

run:
	@echo Starting $(PROJECT_NAME) ...
	$(MANAGE) runserver $(BIND_TO):$(RUNSERVER_PORT)

mailserver:
	python -m smtpd -n -c DebuggingServer $(BIND_TO):$(MAILSERVER_PORT)

syncdb:
	@echo Syncing...
	$(MANAGE) syncdb --noinput
	$(MANAGE) migrate
	$(MANAGE) loaddata $(PROJECT_NAME).json
	@echo Done

shell:
	@echo Starting shell...
	$(MANAGE) shell

testcoverage:
	mkdir -p tests/coverage/modules
	TESTING=1 $(MANAGE) test_coverage $(TEST_OPTIONS) $(TEST_APP)

test:
	TESTING=1 $(MANAGE) test $(TEST_OPTIONS) $(TEST_APP)
	cd wsapi && nosetests

test_web:
	TESTING=1 $(MANAGE) test $(TEST_OPTIONS) $(TEST_APP)

test_api:
	cd wsapi && nosetests -s

test_ui:
	TESTING=1 $(MANAGE) test $(TEST_OPTIONS) $(TEST_UI)

clean:
	@echo Cleaning up...
	find ./$(PROJECT_NAME) | grep '\.pyc$$' | xargs -I {} rm {}
	@echo Done

manage:
ifndef CMD
	@echo Please, spceify -e CMD=command argument to execute
else
	$(MANAGE) $(CMD)
endif

only_migrate:
ifndef APP_NAME
	@echo Please, specify -e APP_NAME=appname argument
else
	@echo Starting of migration of $(APP_NAME)
	$(MANAGE) migrate $(APP_NAME)
	@echo Done
endif

migrate:
ifndef APP_NAME
	$(MANAGE) migrate
else
	@echo Starting of migration of $(APP_NAME)
	$(MANAGE) schemamigration $(APP_NAME) --auto
	$(MANAGE) migrate $(APP_NAME)
	@echo Done
endif

init_migrate:
ifndef APP_NAME
	@echo Please, specify -e APP_NAME=appname argument
else
	@echo Starting init migration of $(APP_NAME)
	$(MANAGE) schemamigration $(APP_NAME) --initial
	$(MANAGE) migrate $(APP_NAME)
	@echo Done
endif

celeryd:
	-@kill -9 `cat $(CELERYD_PID)`
	# -B option is for celerybeat with one worker (scheduling)
	$(MANAGE) celeryd -Q celery -B --pidfile=$(CELERYD_PID) --logfile=$(CELERYD_LOG)&

celeryd_stop:
	-kill -9 `cat $(CELERYD_PID)`

less:
	@grunt-less --config cghub/grunt.js less

minjs:
	@grunt --config cghub/grunt.js min

selectfilters:
	$(MANAGE) selectfilters

selectfilters_clean:
	# clean previously checked filters
	$(MANAGE) selectfilters -c
#
# end targets

