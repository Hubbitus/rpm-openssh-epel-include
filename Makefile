# Makefile for source rpm: openssh
# $Id$
NAME := openssh
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
