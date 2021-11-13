install:
	@echo "Install evolving ..."
	mkdir -p ~/.config/evolving

clean:
	@echo cleaning
	@:

uninstall:
	@echo "Uninstall evolving ..."
	pip uninstall evolving
	rm -rf ~/.config/evolving

