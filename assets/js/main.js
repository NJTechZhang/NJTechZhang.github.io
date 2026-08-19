/* 张荣庭 个人学术主页 - 交互脚本 */
(function () {
  'use strict';

  // 页脚年份自动更新
  document.getElementById('year').textContent = new Date().getFullYear();

  // 移动端导航开关
  var navToggle = document.getElementById('navToggle');
  var navLinks = document.getElementById('navLinks');
  navToggle.addEventListener('click', function () {
    navLinks.classList.toggle('open');
  });

  // 点击导航链接后收起移动端菜单
  navLinks.addEventListener('click', function (e) {
    if (e.target.tagName === 'A') {
      navLinks.classList.remove('open');
    }
  });

  // 导航栏滚动阴影
  var navbar = document.getElementById('navbar');
  window.addEventListener('scroll', function () {
    navbar.style.boxShadow = window.scrollY > 10 ? '0 2px 12px rgba(26,75,140,0.12)' : 'none';
  }, { passive: true });
})();
