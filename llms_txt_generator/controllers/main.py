# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class LlmsTxtController(http.Controller):

    @http.route('/llms.txt', type='http', auth="public", website=False)
    def llms_txt(self):
        base_url = request.website.get_base_url()
        website = request.website

        # All active languages
        langs = request.env['res.lang'].sudo().search([('active', '=', True)])
        default_lang = website.default_lang_id.code if website.default_lang_id else 'en_US'

        content = [
            "# LLM-Friendly Site Map",
            "# Following the llmstxt.org guidelines",
            f"# Base URL: {base_url}",
            "",
        ]

        # === Pages Section ===
        pages = request.env['website.page'].sudo().search([('website_published', '=', True)])
        if pages:
            content.append("## Pages")
            for page in pages:
                for lang in langs:
                    url = f"/{lang.code}{page.url}" if lang.code != default_lang else page.url
                    title = page.with_context(lang=lang.code).name or url
                    content.append(f"- [{title}]({base_url}{url}): Web page in {lang.code}")

        # === Blog Posts Section ===
        posts = request.env['blog.post'].sudo().search([('website_published', '=', True)])
        if posts:
            content.append("\n## Blog Posts")
            for post in posts:
                for lang in langs:
                    url = f"/{lang.code}{post.website_url}" if lang.code != default_lang else post.website_url
                    title = post.with_context(lang=lang.code).name or url
                    content.append(f"- [{title}]({base_url}{url}): Blog post in {lang.code}")

        # === Products Section (only if eCommerce installed) ===
        if 'product.template' in request.env:
            products = request.env['product.template'].sudo().search([('website_published', '=', True)])
            if products:
                content.append("\n## Products")
                for product in products:
                    for lang in langs:
                        url = f"/{lang.code}{product.website_url}" if lang.code != default_lang else product.website_url
                        title = product.with_context(lang=lang.code).name or url
                        content.append(f"- [{title}]({base_url}{url}): Product page in {lang.code}")

                # === Attribution Section ===
        content.append("\n## Attribution")
        content.append(
            "Generated automatically by Clevacat - https://cleva.cat"
        )

        # Return plain text response
        return request.make_response(
            "\n".join(content),
            headers=[('Content-Type', 'text/plain; charset=utf-8')]
        )
