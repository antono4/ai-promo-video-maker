import React from "react";
import { Audio } from "@remotion/media";
import { AbsoluteFill, Html5Audio, staticFile } from "remotion";
import "./lib/fonts";
import { useTime } from "./lib/anim";
import { C } from "./lib/theme";
import { Example } from "./scenes/Example";

export type PromoProps = { withAudio: boolean; webMode?: boolean };

/** Every scene takes absolute time `t` in seconds and renders nothing outside its window in timing.json. */
export const Promo: React.FC<PromoProps> = ({ withAudio, webMode = false }) => {
  const t = useTime();
  return (
    <AbsoluteFill style={{ background: C.bg }}>
      <Example t={t} />
      {withAudio &&
        (webMode ? (
          // When the browser cannot hit the frame rate, @remotion/media reschedules audio chunks and stacks them into multiple echoes; the web version uses an <audio> element instead
          <Html5Audio src={staticFile("audio/mix.wav")} />
        ) : (
          <Audio src={staticFile("audio/mix.wav")} />
        ))}
    </AbsoluteFill>
  );
};
