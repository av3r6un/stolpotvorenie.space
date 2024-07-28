<template>
  <div class="index">
    <curTains />
    <div class="content">
      <div class="content_about">
        <p class="content_about-info">
          Пространство <span class="logo_text">«СТОЛПОТВОРЕНИЕ»</span> является синтезом самых
            разных творческих направлений,<br>таких как:
        </p>
      </div>
      <div class="content_about-aspects">
        <div class="aspect arts">
          <router-link to="/aspect/arts" class="base_link aspect_link">
            <div class="aspect_title">Живопись</div>
            <div class="aspect_image">
              <img src="../assets/imgs/art_image.jpg" alt="arts" class="base_image">
            </div>
          </router-link>
        </div>
        <div class="aspect ceramics">
          <router-link to="/aspect/ceramics" class="base_link aspect_link">
            <div class="aspect_title">Керамика</div>
            <div class="aspect_image">
              <img src="../assets/imgs/ceramics_image.jpg" alt="arts" class="base_image">
            </div>
          </router-link>
        </div>
        <div class="aspect coworking">
          <router-link to="/aspect/coworking" class="base_link aspect_link">
            <div class="aspect_title">Коворкинг</div>
            <div class="aspect_image">
              <img src="../assets/imgs/coworking_image.jpg" alt="arts" class="base_image">
            </div>
          </router-link>
        </div>
        <div class="aspect lecture">
          <router-link to="/aspect/lecture" class="base_link aspect_link">
            <div class="aspect_title">Лекторий</div>
            <div class="aspect_image">
              <img src="../assets/imgs/lecture_image.jpg" alt="arts" class="base_image">
            </div>
          </router-link>
        </div>
        <div class="aspect culture">
          <router-link to="/aspect/culture" class="base_link aspect_link">
            <div class="aspect_title">Культурные мероприятия</div>
            <div class="aspect_image">
              <img src="../assets/imgs/culture_image.jpg" alt="arts" class="base_image">
            </div>
          </router-link>
        </div>
      </div>
      <div class="content_interpret">
        <p class="interpret main_text">
          СТОЛ.ПО.ТВОРЕНИЕ <br>СТО.ЛПОТВОРЕНИЕ <br>СТОЛП.О.ТВОРЕНИЕ <br>СТОЛПОТВОРЕНИЕ
        </p>
        <p class="interpret_about main_text"><span class="long_dash">—</span> можно разбивать слово
            множественными способами, некий каламбур, отражающий нашу философию многогранности.
            Станьте частью нашего творческого тандема, и мы вместе реализуем все ваши самые
            безумные идеи.
        </p>
      </div>
      <div class="content_socials">
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
    </div>
    <div class="content_map">
      Как нас найти?
      <iframe src="https://yandex.ru/map-widget/v1/?um=constructor%3Ae17fe4b6b174ed81e6dcbde44d6cb7bf84b9066b24283e717c13e86c705653f8&amp;source=constructor"
        width="100%" height="400" frameborder="0" title="Как нас найти"></iframe>
    </div>
  </div>
</template>

<script>
import curTains from '../components/curTains.vue';

export default {
  name: 'HomeView',
  components: { curTains },
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
.content{
  font-family: $text-font;
  font-size: 20px;
  &_about{
    max-width: 860px;
    margin: 0 auto;
    text-align: center;
    &-aspects{
      display: grid;
      grid-gap: 10px;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));;
      align-items: flex-start;
      justify-items: center;
      margin-bottom: 50px;
      flex-wrap: wrap;
      .aspect{
        &_title{
          display: flex;
          align-items: center;
          justify-content: center;
          text-align: center;
          font-size: 22px;
          height: 60px;
          text-transform: uppercase;
          color: $black;
          font-weight: 500;
          max-width: 180px;
          font-family: $title-font;
        }
        &_image{
          display: flex;
          aspect-ratio: 9 / 16;
          width: 180px;
          border-radius: 10px;
          box-shadow: 1px 1px 10px 1px rgba($color: $black, $alpha: .5);
          img{
            margin-bottom: 0;
            width: 100%;
            height: 100%;
            border-radius: inherit;
          }
        }
      }
    }
  }
  &_interpret{
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: normal;
    margin-bottom: 50px;
    padding: 0 20px;
    @media screen {
      @media (max-width: 650px) {
        flex-direction: column;
      }
    }
    .interpret{
      font-size: 24px;
      color: $black;
      font-weight: 500;
      font-family: $title-font;
      margin-right: 60px;
      text-align: center;
      @media screen {
        @media (max-width: 650px) {
          margin-bottom: 10px;
          margin-right: 0;
        }
      }
      &_about{
        max-width: 600px;
        width: 60%;
        text-align: justify;
        font-weight: 700;
        font-size: 22px;
        @media screen {
          @media (max-width: 650px) {
            .long_dash{
              display: none;
            }
            max-width: auto;
            width: auto;
          }
        }
      }
    }
  }
  &_socials{
    font-family: $text-font;
    font-weight: 800;
    text-align: center;
    font-size: 24px;
    margin-bottom: 60px;
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
  &_map{
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
}

.contents{
  max-width: 860px;
  text-align: center;
  margin: 0 auto;
  margin-bottom: 30px;
  &_dep{
    list-style-type: none;
    margin-bottom: 30px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    color: $orange;
    font-size: 24px !important;
    li{
      max-width: 205px;
      text-align: center;
    }
  }
  &_interpret{
    margin-right: 60px;
    text-align: center;
    color: $yellow;
  }
  &_about{
    max-width: 600px;
    text-align: justify;
  }
}
.interpret{
  display: flex;
  align-items: center;
  justify-content: center;
}
.main_text{
  font-family: $text-font;
  font-weight: 800;
  font-size: 20px;
}
</style>
