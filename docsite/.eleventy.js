const { EleventyHtmlBasePlugin } = require("@11ty/eleventy");
const syntaxHighlight = require("@11ty/eleventy-plugin-syntaxhighlight");
const codeClipboard = require("eleventy-plugin-code-clipboard");
const pluginMermaid = require("@kevingimbel/eleventy-plugin-mermaid");
const markdownIt = require('markdown-it');

module.exports = (eleventyConfig) => {
  eleventyConfig.addPlugin(syntaxHighlight);
  eleventyConfig.addPlugin(codeClipboard);
  eleventyConfig.addPlugin(pluginMermaid);
	eleventyConfig.addPlugin(EleventyHtmlBasePlugin, {
    baseHref: process.env.DOCSITE_BASE_URL || ""
  });
  eleventyConfig.addPassthroughCopy("data");
  eleventyConfig.addPassthroughCopy("img");
  // Verbs and Workflows are auto-generated
  eleventyConfig.setUseGitIgnore(false);

  const markdownLibrary = markdownIt({
    html: true
  }).use(codeClipboard.markdownItCopyButton);
  
  eleventyConfig.setLibrary("md", markdownLibrary);

  eleventyConfig.addFilter('sortByNavtitle', values => {
    return values.slice().sort((a, b) => a.data.navtitle.localeCompare(b.data.navtitle))
  })
};