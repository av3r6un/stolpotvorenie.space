<template>
  <div class="index">
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
    <div class="socials">
      Мы в соц. сетях:
      <div class="social_links">
        <a href="https://t.me/stolpotvoreniespace" class="base_link">
          <div class="icon tg-icon"></div>
        </a>
        <a href="https://instagram.com/stolpotvorenie.space" class="base_link">
          <div class="icon ig-icon"></div>
        </a>
        <a href="https://vk.com/stolpotvorenie.space" class="base_link">
          <div class="icon vk-icon"></div>
        </a>
      </div>
      <div class="address">
        <a href="https://yandex.ru/maps/-/CDG1IPkG" class="base_link straight_link">
          <div class="icon place-icon"></div>
          Дивенская, 5
        </a>
      </div>
    </div>
    <div class="map">
      Как нас найти?
      <iframe src="https://yandex.ru/map-widget/v1/?um=constructor%3Ae17fe4b6b174ed81e6dcbde44d6cb7bf84b9066b24283e717c13e86c705653f8&amp;source=constructor"
        width="100%" height="400" frameborder="0" title="Как нас найти"></iframe>
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
  margin-top: 40px;
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
.map{
  @media screen {
    @media (max-width: 1024px){
      max-width: 95%;
      margin: 0 auto;
    }
    @media (max-width: 350px) {
      display: none;
    }
  }
  font-family: $text-font;
  font-size: 32px;
  text-align: center;
  iframe{
    border-radius: 5px;
    margin-top: 10px;
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
