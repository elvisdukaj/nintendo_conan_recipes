#include <SDL2/SDL.h>
#include <SDL2/SDL_render.h>
#include <SDL2/SDL_events.h>
#include <cstdio>
#include <cstdlib>

#include <print>
#include <algorithm>

const int SCREEN_WIDTH = 640;
const int SCREEN_HEIGHT = 480;
const float SCREEN_WIDTHf = 640.0f;
const float SCREEN_HEIGHTf = 480.0f;

struct vec2 {
  float x;
  float y;

  vec2 &operator*=(float scalar) {
    x *= scalar;
    y *= scalar;
    return *this;
  }

  vec2 &operator+=(vec2 v) {
    x += v.x;
    y += v.y;
    return *this;
  }
};

vec2 operator+(vec2 lhs, vec2 rhs) {
  return vec2{lhs.x + rhs.x, lhs.y + rhs.y};
}

class Ball {
public:
  Ball() : m_rect{.x = 10, .y = 10, .w = 10, .h = 10}, m_dir{1.0f, 1.3f} {}

  void update() {
    auto pos = vec2{static_cast<float>(m_rect.x), static_cast<float>(m_rect.y)};
    pos += m_dir;

    if (pos.x > SCREEN_WIDTH - m_rect.w || pos.x < 0.0f) {
      m_dir.x *= -1;
    }
    if (pos.y > SCREEN_HEIGHT - m_rect.h || pos.y < 0) {
      m_dir.y *= -1;
    }

    pos.x = std::clamp(pos.x, 0.0f, SCREEN_WIDTHf - m_rect.w);
    pos.y = std::clamp(pos.y, 0.0f, SCREEN_HEIGHTf - m_rect.h);

    m_rect.x = static_cast<float>(pos.x);
    m_rect.y = static_cast<float>(pos.y);
  }

  void draw(SDL_Renderer* ren) {
      SDL_SetRenderDrawColor(ren, 0, 255, 125, 255);
      SDL_RenderFillRect(ren, &m_rect);
  }

private:
  SDL_Rect m_rect;
  vec2 m_dir;
};

int main(int argc, char *argv[]) {
  if (SDL_Init(SDL_INIT_EVERYTHING) != 0) {
    std::println("SDL_Init Error: {}", SDL_GetError());
    return EXIT_FAILURE;
  }

  SDL_Window *win = SDL_CreateWindow("Hello World!", 0, 0, SCREEN_WIDTH,
                                     SCREEN_HEIGHT, SDL_WINDOW_SHOWN);
  if (win == NULL) {
    std::println("SDL_CreateWindow Error: {}", SDL_GetError());
    return EXIT_FAILURE;
  }

  SDL_Renderer *ren = SDL_CreateRenderer(
      win, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
  if (ren == NULL) {
    std::println("SDL_CreateRenderer Error: {}", SDL_GetError());
    SDL_DestroyWindow(win);
    SDL_Quit();
    return EXIT_FAILURE;
  }

  Ball ball;

  while (true) {
    auto isRunning = true;
    SDL_Event event;
    while (isRunning) {
      // poll and handle events from the SDL framework.
      while (SDL_PollEvent(&event) != 0) {
        switch (event.type) {
        case SDL_QUIT:
          isRunning = false;
          break;
        }
      }

      SDL_SetRenderDrawColor(ren, 255, 0, 0, 255);
      SDL_RenderClear(ren);

      ball.update();
      ball.draw(ren);

      SDL_RenderPresent(ren);
    }
  }

  SDL_DestroyRenderer(ren);
  SDL_DestroyWindow(win);
  SDL_Quit();
  return 0;
}

