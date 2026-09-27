# frozen_string_literal: true

Jekyll::Hooks.register [:posts, :pages, :documents], :post_render do |item|
  next unless item.output_ext == ".html"
  next unless item.output&.include?("<table")

  item.output = item.output.gsub(/(?:<div class="table-wrapper">\s*)?(<table(?:\s+[^>]*)?>[\s\S]*?<\/table>)(?:\s*<\/div>)?/) do
    "<div class=\"table-wrapper\">#{$1}</div>"
  end
end
