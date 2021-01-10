# extract <QuerySet> iterator elements to a list with their
# names
def queryset_ext(qs):
  result = ''
  l_qs = len(qs)
  for i in range(l_qs):
    if i != l_qs - 1:
      result += qs[i] + ','
    else:
      result += qs[i]
  return result


# returns the list of pages from paginator for rendering
# in template
def pages_list(paginator, page_number):
  result = []
  n = paginator.num_pages
  result += max_pag_size(page_number, 6)

  for i in range(len(result) - 1, 0, -1):
    if result[i] > n:
      del result[i]
  return result

# determine a maximum number of pages for pagination 
# for rendering, this will ensure a better UI
def max_pag_size(current_page, size):
  result = []
  anchor = int((int(current_page) - 1) / size)
  for i in range(size):
    result.append((anchor * size) + i + 1)
  return result

# returns first n elements of a text as a new text
def text_splitter(text, n):
  first_n_words = text.split()[:n]
  result = ' '.join(first_n_words)
  return result