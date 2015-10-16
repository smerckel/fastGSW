#
#
#

PREFIX:=/usr/local

Program:=gsw_vector_check

CFLAGS:=	-O3
CINCLUDES:=	-I. -I../gsw_c_v3.05
#CLIBRARIES:=	-L../gsw_c_v3.05
Library:=	libgsw_vector.so

$(Library)_SRCS:=	gsw_vector.c
$(Library)_OBJS:=	gsw_vector.o

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
	gcc -shared -o $(Library) $($(Library)_OBJS) $(CLIBRARIES) -lm -lgswteos-10

clean:
	rm -f $(Program) $(Library) $($(Library)_OBJS)  $($(Program)_OBJS) 

install:
	install -m 0755 $(Library) $(PREFIX)/lib
	ldconfig $(PREFIX)/lib

