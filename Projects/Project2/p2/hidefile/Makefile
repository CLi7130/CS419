all:	hidefile.so

hidefile.so:	hidefile.c
	gcc -shared -fPIC hidefile.c -o hidefile.so -ldl

clean:
	rm -f hidefile.so secret-1.txt secret-2.txt test1.txt test2.txt test3.txt test4.txt

test:	all
	@ echo creating "secret-1.txt"; echo "this file is hidden" >secret-1.txt
	@ echo creating "secret-2.txt"; echo "this file is also hidden" >secret-2.txt
	@ echo "hiding secret-1"
	export HIDDEN=secret-1.txt LD_PRELOAD=$$PWD/hidefile.so; ls -l
	@ echo "hiding secret-2"
	export HIDDEN=secret-2.txt LD_PRELOAD=$$PWD/hidefile.so; ls -l
	@ echo "hiding nothing"
	unset HIDDEN
	LD_PRELOAD=$$PWD/hidefile.so; ls -l

test2: hidefile.so
	@ echo creating "secret-1.txt"; echo "this file is hidden" >secret-1.txt
	@ echo creating "secret-2.txt"; echo "this file is also hidden" >secret-2.txt
	@echo creating "test-1.txt"; echo "test-1" > test-1.c
	@echo creating "test2.txt"; echo "test2" > test2.txt
	@echo creating "test3.txt"; echo "test3" > test3.txt
	@echo creating "test4.txt"; echo "test4" > test4.txt

	@ echo "hiding secret-1"
	export HIDDEN=secret-1.txt LD_PRELOAD=$$PWD/hidefile.so; ls -l
	@ echo "hiding secret-2"
	export HIDDEN=secret-2.txt LD_PRELOAD=$$PWD/hidefile.so; ls -l

	@echo "hiding test1, test2, test3, test4"
	export HIDDEN=test2.txt:test-1.c:test3.txt:test4.txt LD_PRELOAD=$$PWD/hidefile.so; ls -l
	@ echo "hiding nothing"
	unset HIDDEN
	LD_PRELOAD=$$PWD/hidefile.so; ls -l