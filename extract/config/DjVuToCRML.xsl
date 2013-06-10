<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="1.0">
    <xsl:output method="xml" indent="yes"/>
    
    <!-- Adding an empty fonttbl node, will have to look at other examples to extract this -->
    <xsl:template match="/">
        <xsl:element name="document">
        <xsl:element name="fonttbl"/>
            <xsl:for-each select="//OBJECT">
                <xsl:element name="page">    
                    <xsl:attribute name="w">
                        <xsl:value-of select="@width"/>
                    </xsl:attribute>
                    <xsl:attribute name="h">
                        <xsl:value-of select="@height"/>
                    </xsl:attribute>
                    <xsl:attribute name="id">
                        <xsl:value-of select="position() - 1"/>
                    </xsl:attribute>
                    <xsl:attribute name="key">
                        <xsl:value-of select="position() - 1"/>
                    </xsl:attribute>
                    <xsl:attribute name="label">
                        <xsl:choose>
                            <xsl:when test="HIDDENTEXT/PAGECOLUMN/REGION/PARAGRAPH/*">
                                <xsl:text>PT_CHAPTER</xsl:text>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:text>PT_EMPTY</xsl:text>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:attribute>
                    <xsl:attribute name="pageNumber">
                        <xsl:text>I-N</xsl:text>
                    </xsl:attribute>
                    <xsl:apply-templates select="HIDDENTEXT/PAGECOLUMN/REGION/PARAGRAPH"/>
                </xsl:element>
            </xsl:for-each>
        </xsl:element>
    </xsl:template>
    
    <xsl:template match="HIDDENTEXT/PAGECOLUMN/REGION/PARAGRAPH">
        <xsl:if test="child::node()">
            <xsl:element name="region">
                <!-- Must figure out section attributes as far as id and key -->
                <xsl:element name="section">
                    <xsl:attribute name="id">
                        <xsl:text>0</xsl:text>
                    </xsl:attribute>
                    <xsl:attribute name="label">
                        <xsl:text>SEC_BODY</xsl:text>
                    </xsl:attribute>
                    <xsl:apply-templates select="LINE"/>
                </xsl:element>
            </xsl:element>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="LINE">
        <xsl:element name="line">
            <xsl:value-of select="normalize-space(.)"/>
        </xsl:element>
    </xsl:template>    
</xsl:stylesheet>
