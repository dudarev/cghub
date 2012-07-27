PYTHONPATH=$(CURDIR):$(CURDIR)/../../wsapi/

PYTHON= PYTHONPATH=$(PYTHONPATH) python

STATS_DIR=stats
IMGS_DIR=imgs
QUERIES_COUNT=100

THREE_POS_FILENAME_PREFIX=three_pos_queries
FOUR_POS_FILENAME_PREFIX=four_pos_queries

get_gprof2dot:
	@wget -O gprof2dot http://gprof2dot.jrfonseca.googlecode.com/git/gprof2dot.py
	@chmod +x gprof2dot

profile_api:
	$(PYTHON) profile_api.py $(QUERIES_COUNT)

profile_api_call_graph:
	@./gprof2dot -f pstats $(STATS_DIR)/$(THREE_POS_FILENAME_PREFIX)_with_cache.stats -n0.1 -e0.1 | dot -Tpng -o $(IMGS_DIR)/$(THREE_POS_FILENAME_PREFIX)_with_cache.png
	@./gprof2dot -f pstats $(STATS_DIR)/$(THREE_POS_FILENAME_PREFIX)_without_cache.stats -n0.1 -e0.1 | dot -Tpng -o $(IMGS_DIR)/$(THREE_POS_FILENAME_PREFIX)_without_cache.png
	@./gprof2dot -f pstats $(STATS_DIR)/$(FOUR_POS_FILENAME_PREFIX)_with_cache.stats -n0.1 -e0.1 | dot -Tpng -o $(IMGS_DIR)/$(FOUR_POS_FILENAME_PREFIX)_with_cache.png
	@./gprof2dot -f pstats $(STATS_DIR)/$(FOUR_POS_FILENAME_PREFIX)_without_cache.stats -n0.1 -e0.1 | dot -Tpng -o $(IMGS_DIR)/$(FOUR_POS_FILENAME_PREFIX)_without_cache.png
	@echo 'Call graphs are generated for profilers stats.'

profile_api_plot:
	@$(PYTHON) plot.py $(STATS_DIR)/$(THREE_POS_FILENAME_PREFIX)_with_cache.csv $(IMGS_DIR)/$(THREE_POS_FILENAME_PREFIX)_with_cache_plot.png
	@$(PYTHON) plot.py $(STATS_DIR)/$(THREE_POS_FILENAME_PREFIX)_without_cache.csv $(IMGS_DIR)/$(THREE_POS_FILENAME_PREFIX)_without_cache_plot.png
	@$(PYTHON) plot.py $(STATS_DIR)/$(FOUR_POS_FILENAME_PREFIX)_with_cache.csv $(IMGS_DIR)/$(FOUR_POS_FILENAME_PREFIX)_with_cache_plot.png
	@$(PYTHON) plot.py $(STATS_DIR)/$(FOUR_POS_FILENAME_PREFIX)_without_cache.csv $(IMGS_DIR)/$(FOUR_POS_FILENAME_PREFIX)_without_cache_plot.png
	@echo 'Plots has been generated for profilers stats.'

copy_imgs:
	@cp imgs/* ../../docs/source/imgs/
