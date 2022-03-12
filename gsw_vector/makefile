#
#
#

MAJOR_VERSION:=0
MINOR_VERSION:=1


PREFIX:=/usr/local/lib

Program:=gsw_vector_check

CFLAGS:=	-O3
CINCLUDES:=	-I. 
CLIBRARIES:=    -L$(PREFIX)
Library:=	libgsw_vector.so

$(Library)_SRCS:=	gsw_vector.c
$(Library)_OBJS:=	gsw_vector.o
$(Library)_HDRS:=	gsw_vector.h

$(Program)_SRCS:=	gsw_vector_check.c
$(Program)_OBJS:=	gsw_vector_check.o

.PHONY: install

all:	$(Library)

program:	$(Program)

library:	$(Library)


$(Program):	$($(Program)_SRCS)
	gcc $(CFLAGS) $(CINCLUDES) -o $(Program) $($(Program)_SRCS) -lm -lgsw_vector -lgswteos-10


$(Library):	$($(Library)_SRCS)
	gcc -fPIC -c $(CFLAGS) $(CINCLUDES) $($(Library)_SRCS) 
	gcc -shared -Wl,-soname,$(Library) -o $(Library).$(MAJOR_VERSION).$(MINOR_VERSION)  $($(Library)_OBJS) $(CLIBRARIES) -lm -lgswteos-10

clean:
	rm -f $(Program) $(Library) $($(Library)_OBJS)  $($(Program)_OBJS) 

install:
	install -m 0755 $(Library).$(MAJOR_VERSION).$(MINOR_VERSION) $(PREFIX)
	install -m 0755 $($(Library)_HDRS) $(PREFIX)/include
	ldconfig -n $(PREFIX)
	ldconfig

