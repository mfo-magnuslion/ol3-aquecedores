/* Medição do Google Ads: conta AW-18556764042.
   Conversão "Clique no WhatsApp": dispara quando alguém clica em qualquer link wa.me do site. */
(function () {
  var ID = "AW-18556764042";
  var CONVERSAO = ID + "/b7-6CL-AprIdEIr_xpBF";

  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };
  window.gtag("js", new Date());
  window.gtag("config", ID);

  var s = document.createElement("script");
  s.async = true;
  s.src = "https://www.googletagmanager.com/gtag/js?id=" + ID;
  document.head.appendChild(s);

  document.addEventListener("click", function (e) {
    var a = e.target && e.target.closest ? e.target.closest("a[href]") : null;
    if (!a) return;
    var href = a.getAttribute("href") || "";
    if (href.indexOf("https://wa.me/") !== 0 && href.indexOf("https://api.whatsapp.com/") !== 0) return;
    window.gtag("event", "conversion", { send_to: CONVERSAO });
  }, true);
})();
