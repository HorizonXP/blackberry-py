QMAKE_TARGET  = TartStart
PROJECT_DIR	  := $(dir $(word $(words $(MAKEFILE_LIST)),$(MAKEFILE_LIST)))
I18N_DIR	  := $(PROJECT_DIR)/translations
DEPLOYDIR     = ../tart/entry

include mk/cs-base.mk

all: FORCE Device-Release Device-Debug Simulator-Debug

install: FORCE
	"mkdir" -p $(DEPLOYDIR)
	cp arm/o.le-v7-g/TartStart $(DEPLOYDIR)
	cp arm/o.le-v7/TartStart.so $(DEPLOYDIR)
	cp x86/o-g/TartStart $(DEPLOYDIR)/TartStart-x86

	ntoarm-strip $(DEPLOYDIR)/TartStart
	ntoarm-strip $(DEPLOYDIR)/TartStart.so
	ntox86-strip $(DEPLOYDIR)/TartStart-x86
