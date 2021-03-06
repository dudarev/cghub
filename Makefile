# constants
#

include Makefile.def

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
	TESTING=1 $(MANAGE) test --verbosity 2 $(TEST_OPTIONS) $(TEST_APP)

test_ui:
	TESTING=1 $(MANAGE) test --verbosity 2 $(TEST_OPTIONS) $(TEST_UI)

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

update_full_metadata_cache:
	$(MANAGE) update_full_metadata_cache

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

less:
	grunt --gruntfile cghub/Gruntfile.js recess

minjs:
	grunt --gruntfile cghub/Gruntfile.js uglify

selectoptions:
	$(MANAGE) selectoptions

searchoptions:
	$(MANAGE) searchoptions

##
# cghub specific setup targets.
cghub-setup:
	@[ $$EUID == 0 ]  || (echo "cghub-setup target must be run as root" >/dev/stderr; exit 1)
	mkdir -p ${CACHE_DIR}
	chown ${cghubuser}:${cghubwwwgrp} ${CACHE_DIR}
	chmod g+rwxs ${CACHE_DIR}
	mkdir -p ${PIDS_DIR} ${LOGS_DIR}
	chown ${cghubuser}:${cghubgrp} ${PIDS_DIR} ${LOGS_DIR}
	chown ${cghubuser}:${cghubdevgrp} ${CGHUB_APPROOT_DIR}
	chmod g+rwxs ${CGHUB_APPROOT_DIR}
	chown ${cghubuser}:${cghubdevgrp} ${CGHUB_APP_DIR}
	find ${CGHUB_APP_DIR} -type d |xargs chmod g+rwxs
	chmod -R g+w ${CGHUB_APP_DIR}

# restart all daemons
restart: http_restart

# restart http [checks for FreeBSD and Linux]
http_restart:
ifneq ($(wildcard /usr/local/etc/rc.d/apache22),)
	sudo /usr/local/etc/rc.d/apache22 restart
else
	sudo /etc/init.d/httpd restart
endif

#
# end targets

