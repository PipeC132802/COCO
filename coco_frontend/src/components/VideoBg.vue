<template>
  <div class="video-bg">
    <div id="video-overlay"></div>
    <video
      id="video_background"
      playsinline="playsinline"
      autoplay="autoplay"
      muted="muted"
      loop="loop"
      style="overflow: hidden"
    >
      <source
        src="../assets/videos/Coco_background_video.mp4"
        type="video/mp4"
        style="overflow: hidden"
      />
    </video>
  </div>
</template>

<script>
export default {
  name: "VideoBg",
};
</script>

<style>
#video-overlay {
  background: rgba(0, 0, 0, 0.5);
  position: fixed;
  left: 0px;
  top: 0px;
  width: 100vw;
  z-index: 1;
  height: 100%;
  overflow: hidden;
}
#video_background {
  position: fixed;
  min-height: 100vh;
  min-width: 100vw;
  width: auto;
  height: auto;
  left: 0px;
  top: 0px;
  z-index: 0;
  overflow: hidden;
}
</style>