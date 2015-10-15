#
#
#

PREFIX:=/usr/local


CFLAGS:=	-O3
CINCLUDES:=	-I. -I../gsw_c_v3.05
#CLIBRARIES:=	-L../gsw_c_v3.05
Library:=	libgsw_vector.so

$(Library)_SRCS:=	gsw_vector.c
$(Library)_OBJS:=	gsw_vector.o

.PHONY: install

all:	$(Library)

library:	$(Library)

$(Library):	$($(Library)_SRCS)
	gcc -fPIC -c $(CFLAGS) $(CINCLUDES) $($(Library)_SRCS) 
	gcc -shared -o $(Library) $($(Library)_OBJS) $(CLIBRARIES) -lm -lgswteos-10

clean:
	rm -f $(Program) $(Library) $($(Library)_OBJS)

install:
	install -m 0755 $(Library) $(PREFIX)/lib
	ldconfig $(PREFIX)/lib

