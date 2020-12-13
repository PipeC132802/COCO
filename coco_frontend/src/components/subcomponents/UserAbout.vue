<template>
  <v-card>
    <blockquote class="blockquote">
      <p class="mb-0">
        Creativity is just connecting things. When you ask creative people how
        they did something, they feel a little guilty because they didn't really
        do it, they just saw something. It seemed obvious to them after a while.
        That's because they were able to connect experiences they've had and
        synthesize new things.
      </p>
      <footer class="blockquote-footer">
        Steve Jobs <cite title="Source Title">Source Title</cite>
      </footer>
    </blockquote>
  </v-card>
</template>

<script>
export default {};
</script>

<style>
.blockquote {
  font-size: 1.25rem;
  border: 1px solid rgba(222, 226, 230, 0.54);
  border-left: 0.5rem solid rgba(0, 123, 255, 0.54);
  color: #6c757d;
  font-family: "Open Sans", "Segoe UI", "Roboto", "Helvetica Neue", "Arial",
    "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji",
    "Segoe UI Symbol", "Noto Color Emoji";
  font-style: italic;
  line-height: 1.6;
  margin: 1.875rem auto;
  max-width: 60%;
  padding: 4.6875rem 1.875rem 1.875rem 4.6875rem;
  position: relative;
  width: 100%;
}
.blockquote:before {
  font-size: 6.875rem;
  color: rgba(0, 123, 255, 0.54);
  content: "\201C";
  font-family: "Noto Serif", "Georgia", "Times New Roman", "Times", serif;
  font-size: 5.5rem;
  height: 3.75rem;
  left: 0.9375rem;
  line-height: 1;
  max-width: 3.75rem;
  position: absolute;
  text-align: inherit;
  top: 0.9375rem;
  width: 100%;
}
.blockquote:after {
  content: "";
}
</style>