<template>
  <footer class="footer mt-auto">
    <div class="footer__items d-flex align-items-center m-0">
      <p class="m-0 mr-1">Destacame</p>
      <p class="m-0 second-text">Test</p>
      <p class="m-0 second-text">&nbsp;{{ year }}</p>
    </div>
    <div class="icons__container">
      <a href="https://github.com/JorgePov" target="_blank">
        <b-icon class="icons" icon="github"></b-icon>
      </a>
      <a href="https://www.linkedin.com/in/jorge-poveda/" target="_blank">
        <b-icon class="icons" icon="linkedin"></b-icon>
      </a>
    </div>
  </footer>
</template>
<script>
export default {
  data() {
    const year = new Date().getFullYear();
    return {
      year: year,
    };
  },
  name: "Footer",
};
</script>
<style lang="scss">
.footer {
  background-color: #505659;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  & > hr {
    width: 50%;
    border: 1px dotted;
  }
}

.icons__container {
  display: flex;
  gap: 20px;
  align-items: center;
  font-size: 30px;

  & > .icons {
    cursor: pointer;
  }
}

.footer__items {
  & > p:first-child {
    color: white;
  }

  & > p {
    font-size: 20px;
  }
}
</style>