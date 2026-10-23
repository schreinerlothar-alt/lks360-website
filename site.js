// Inventory filter and contact form (static site, no server).
(function () {
  var qs = new URLSearchParams(location.search);

  var list = document.getElementById('ulist');
  if (list) {
    var units = Array.prototype.slice.call(list.querySelectorAll('.unit'));
    var f = { q: 'q', cat: 'fcat', make: 'fmake', hz: 'fhz', mw: 'fmw', sort: 'fsort' };
    Object.keys(f).forEach(function (k) { f[k] = document.getElementById(f[k]); });
    if (qs.get('cat')) f.cat.value = qs.get('cat');
    if (qs.get('make')) f.make.value = qs.get('make');

    var apply = function () {
      var q = f.q.value.trim().toLowerCase(), shown = 0;
      var range = f.mw.value ? f.mw.value.split('-').map(Number) : null;
      units.forEach(function (u) {
        var d = u.dataset, mw = d.mw === '' ? null : Number(d.mw);
        var ok = (!q || d.text.indexOf(q) > -1) &&
          (!f.cat.value || d.cat === f.cat.value) &&
          (!f.make.value || d.make === f.make.value) &&
          (!f.hz.value || d.hz.indexOf(f.hz.value) > -1) &&
          (!range || (mw !== null && mw >= range[0] && mw < range[1]));
        u.hidden = !ok;
        if (ok) shown++;
      });
      var sorted = units.slice();
      if (f.sort.value) {
        var dir = f.sort.value === 'asc' ? 1 : -1;
        sorted.sort(function (a, b) {
          var x = a.dataset.mw === '' ? null : Number(a.dataset.mw), y = b.dataset.mw === '' ? null : Number(b.dataset.mw);
          if (x === null) return 1;
          if (y === null) return -1;
          return (x - y) * dir;
        });
      }
      sorted.forEach(function (u) { list.appendChild(u); });
      document.getElementById('count').textContent = shown + (shown === 1 ? ' unit' : ' units');
      document.getElementById('empty').hidden = shown > 0;
    };
    Object.keys(f).forEach(function (k) { f[k].addEventListener('input', apply); });
    apply();
  }

  var form = document.getElementById('mailform');
  if (form) {
    if (qs.get('unit') && form.unit) form.unit.value = qs.get('unit');
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var lines = [];
      Array.prototype.forEach.call(form.elements, function (el) {
        if (el.name && el.value) lines.push((el.dataset.label || el.name) + ': ' + el.value);
      });
      var subject = (form.dataset.subject || 'Inquiry') + (form.company && form.company.value ? ' from ' + form.company.value : '');
      location.href = 'mailto:manager@lks360.com?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(lines.join('\n'));
      var note = document.getElementById('formnote');
      if (note) note.hidden = false;
    });
  }
})();
