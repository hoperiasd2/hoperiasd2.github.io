// 강의록 아카이브: 목록 검색 + 목차 현재 위치 표시
(function () {
  var q = document.getElementById('q');
  if (q) {
    q.addEventListener('input', function () {
      var term = q.value.trim().toLowerCase();
      document.querySelectorAll('.card').forEach(function (card) {
        var hits = 0;
        card.querySelectorAll('li[data-q]').forEach(function (li) {
          var ok = !term || li.getAttribute('data-q').indexOf(term) !== -1;
          li.classList.toggle('is-hidden', !ok);
          if (ok) hits++;
        });
        card.classList.toggle('is-hidden', term && hits === 0);
        if (term) card.open = hits > 0;
      });
    });
  }
  if (location.hash) {
    var d = document.getElementById(location.hash.slice(1));
    if (d && d.tagName === 'DETAILS') d.open = true;
  }

  var links = document.querySelectorAll('.toc a[href^="#"]');
  if (!links.length || !('IntersectionObserver' in window)) return;
  var map = {};
  links.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) {
        links.forEach(function (a) { a.classList.remove('is-active'); });
        var a = map[e.target.id];
        if (a) a.classList.add('is-active');
      }
    });
  }, { rootMargin: '0px 0px -70% 0px' });
  Object.keys(map).forEach(function (id) {
    var el = document.getElementById(id);
    if (el) io.observe(el);
  });
})();
