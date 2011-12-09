##
## Resources
##
NAME=tenants
DOCBOOK_SCHEMA=rng/docbook.rng
FOP_XSLT=xsl/auth-blueprint-fo.xsl
XSLTHL_CONFIG=file://$(shell pwd)/xsl/docbook/highlighting/xslthl-config.xml

##
## ClassPath
##
CP= jars/saxon.jar:jars/saxon65.jar:jars/xslthl-2.0.2.jar

##
##  Images
##
SVGS=
STATIC_SVGS=images/TenantModel4.svg
STATIC_SAMPLES=samples/move.xml samples/tenant.wadl

##
## Commands
##
XMLLINT=xmllint
OPEN=open
FOP=fop
DOT=dot
JAVA=java

$(NAME).pass1 : $(NAME).xml $(SVGS) $(STATIC_SVGS) $(STATIC_SAMPLES)
	$(XMLLINT) --xinclude --relaxng $(DOCBOOK_SCHEMA) $(NAME).xml > $(NAME).pass1

view : $(NAME).pdf
	$(OPEN) $(NAME).pdf

$(NAME).pdf : $(NAME).fo
	$(FOP) $(NAME).fo $(NAME).pdf

$(NAME).fo : $(NAME).pass1 $(FOP_XSLT)
	$(JAVA) -cp $(CP) -Dxslthl.config="$(XSLTHL_CONFIG)" com.icl.saxon.StyleSheet -o $(NAME).fo $(NAME).pass1 $(FOP_XSLT)

$(SVGS): %.svg: %.dot
	$(DOT) -Tsvg -o$@ $<

clean:
	rm -f $(NAME).pass1 $(NAME).pdf $(NAME).fo $(SVGS)
