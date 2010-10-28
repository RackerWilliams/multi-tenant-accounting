<xsl:stylesheet exclude-result-prefixes="d"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:d="http://docbook.org/ns/docbook"
                xmlns:fo="http://www.w3.org/1999/XSL/Format"
                version="1.0">

    <xsl:import href="docbook/fo/docbook.xsl" />
    <xsl:import href="docbook/fo/highlight.xsl"/>

  <!--
      XSL-FO Extensions:

      These are used to do things like generate PDF Bookmarks, which
      are out of scope in standard XSL-FO 1.0, but which most XSL-FO
      solutions support via Extensions.

      XSL-FO 1.1, addresses the issue of bookmarks, with a new
      bookmark element, Apache FOP version > 0.90 supports XSL-FO 1.1.

      Enable 1 and only 1 extension, depending on the XSL-FO
      implementation.
  -->
  <xsl:param name="fop1.extensions" select="1"/> <!-- Apache FOP >= 0.90 -->
  <xsl:param name="fop.extensions"  select="0"/> <!-- Apache FOP < 0.90 -->
  <xsl:param name="axf.extensions"  select="0"/> <!-- Antenna House's XSL Formatter -->
  <xsl:param name="xep.extensions"  select="0"/> <!-- RenderX's XEP -->

  <xsl:param name="use.extensions" select="1"/>
  <xsl:param name="callouts.extension" select="1"/>
  <xsl:param name="textinsert.extension" select="1"/>

  <!-- Define hard pagebreak -->
  <xsl:template match="processing-instruction('hard-pagebreak')">
    <fo:block break-after='page'/>
  </xsl:template>

  <!-- Admonition Graphics -->
  <xsl:param name="admon.graphics" select="1"/>
  <xsl:param name="admon.graphics.path" select="'images/docbook/'"/>
  <xsl:param name="admon.graphics.extension" select="'.svg'"/>

  <!-- Watermark -->
  <xsl:param name="draft.watermark.image" select="'images/Draft.svg'"/>

  <!-- Callout Graphics -->
  <xsl:param name="callout.unicode"  select="0"/>
  <xsl:param name="callout.graphics" select="1"/>
  <xsl:param name="callout.graphics.extension" select="'.svg'"/>
  <xsl:param name="callout.graphics.path" select="'images/callouts/'"/>
  <xsl:param name="callout.graphics.number.limit" select="30"/>

  <!-- Source Code Properties -->
  <xsl:param name="shade.verbatim" select="1"/>
  <xsl:param name="highlight.source" select="1"/>

  <!-- Bibliography customization -->
  <xsl:param name="bibliography.numbered" select="1"/>

  <!-- Customize Inline -->
  <xsl:template match="d:token">
      <xsl:call-template name="inline.monoseq"/>
  </xsl:template>

</xsl:stylesheet>
