CFLAGS = -std=c99 -g -Wall -Wextra -Werror -pedantic
LDLIBS = -lm

all: armstrong libarmstrong.so

armstrong: armstrong.c
	$(CC) $(CFLAGS) $< -o $@ $(LDLIBS)

# Loaded by the unit tests to call is_armstrong directly.
libarmstrong.so: armstrong.c
	$(CC) $(CFLAGS) -shared -fPIC $< -o $@ $(LDLIBS)

# Run by the Quiz platform before the tests: a fresh build without -Werror,
# so a warning does not keep the program from being tested.
prepare:
	$(MAKE) --always-make all CFLAGS="$(filter-out -Werror,$(CFLAGS))"

test: all
	pytest -vv

format:
	clang-format --dry-run --Werror armstrong.c

clean:
	$(RM) armstrong libarmstrong.so report.xml

.PHONY: all prepare test format clean
