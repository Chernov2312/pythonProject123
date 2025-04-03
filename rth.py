print("&".join("https://online.minjust.gov.kg/user/search?activity=01_49_0&operator=AND&page=0&size=50".split("&")[:2]) +
      "&" + "https://online.minjust.gov.kg/user/search?activity=01_49_0&operator=AND&page=0&size=50".split("&")[2].split("=")[
          0] + "=&" + "https://online.minjust.gov.kg/user/search?activity=01_49_0&operator=AND&page=0&size=50".split("&")[3])
print("https://online.minjust.gov.kg/user/search?activity=01_49_0&operator=AND&page=0&size=50".split("&"))