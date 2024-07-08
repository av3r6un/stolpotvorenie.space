<template>
  <div class="index">
    <div class="socials">
      Мы в соц. сетях:
      <div class="social_links">
        <a href="https://t.me" class="base_link">
          <div class="icon tg-icon"></div>
        </a>
        <a href="https://instagram.com" class="base_link">
          <div class="icon ig-icon"></div>
        </a>
        <a href="https://vk.com" class="base_link">
          <div class="icon vk-icon"></div>
        </a>
      </div>
      <div class="address">
        <a href="https://yandex.ru/maps/-/CDGVI2Ym" class="base_link straight_link">
          <div class="icon place-icon"></div>
          Дивенская, 5
        </a>
      </div>
    </div>
    <div class="some_info">
      <p class="balamutki">
        Утки баламутки грызут апельсинки Утки баламутки грызут апельсинки Утки баламутки грызут
         апельсинки Утки баламутки грызут апельсинки Утки баламутки грызут апельсинки
         Утки баламутки грызут апельсинки Утки баламутки грызут апельсинки Утки баламутки грызут
         апельсинки. Утки баламутки грызут апельсинки Утки баламутки грызут апельсинки Утки
         баламутки грызут апельсинки. Утки баламутки грызут апельсинки Утки баламутки грызут
         апельсинки Утки баламутки грызут апельсинки
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  data() {
    return {};
  },
};
</script>
<style lang="scss" scoped>
@import "@/assets/variables.scss";
.index{
  margin: 0 auto;
  max-width: 1024px;
  color: $white;
  padding: 60px 0;
  @media screen {
    @media (max-width: 500px) {
      max-width: 95%;
    }
  }
}
.socials{
  font-family: $text-font;
  font-weight: 800;
  text-align: center;
  font-size: 24px;
  margin-bottom: 40px;
  .social_links{
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 40px 0 20px 0;
  }
  .address{
    display: flex;
    justify-content: center;
    .icon{
      max-width: 50px;
    }
  }
}
.some_info{
  margin: 0 auto;
}
.balamutki{
  font-family: $text-font;
  font-weight: 800;
  font-size: 20px;
  max-width: 860px;
  text-align: center;
  margin: 0 auto;
}
</style>
