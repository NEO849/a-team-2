// Tracebound hero, project-track (React + motion/react).
// Design language identical to the artifact build; here motion is JS-driven and interruptible.
// Rules applied: transform/opacity only, easing [0.16,1,0.3,1], UI durations < 500ms,
// full transform strings (not x/y shorthands), reduced-motion, hover gated by pointer.
// GSAP ScrollTrigger is reserved for real pin/scrub work; a reveal only needs whileInView.
import { motion, useReducedMotion } from "motion/react";

const EASE = [0.16, 1, 0.3, 1] as const;

const HOPS = [
  { x: 40, y: 235, ms: 3 }, { x: 140, y: 150, ms: 11 }, { x: 250, y: 205, ms: 18 },
  { x: 350, y: 95, ms: 27 }, { x: 450, y: 160, ms: 41 }, { x: 520, y: 70, ms: 63 },
];
const POINTS = HOPS.map((h) => `${h.x},${h.y}`).join(" ");
const hopColor = (ms: number) =>
  ms < 15 ? "var(--signal-fast)" : ms < 35 ? "var(--signal-mid)" : "var(--signal-slow)";

const WORDS = ["See", "every", "hop", "before", "users", "feel", "it."];

export function Hero() {
  const reduce = useReducedMotion();

  return (
    <section className="hero">
      <div className="lede">
        <h1>
          {WORDS.map((w, i) => (
            <motion.span
              key={i}
              style={{ display: "inline-block", marginRight: "0.28ch" }}
              initial={reduce ? false : { opacity: 0, transform: "translateY(14px)" }}
              animate={{ opacity: 1, transform: "translateY(0px)" }}
              transition={{ duration: 0.46, delay: 0.12 + i * 0.055, ease: EASE }}
            >
              {w}
            </motion.span>
          ))}
        </h1>

        <p className="sub">
          Live path tracing with per hop latency, ASN and geo. Watch the route form in real time,
          not after the incident.
        </p>

        <div className="cta-row">
          {/* press + hover gated; hover variant only fires on fine pointers via CSS media in the stylesheet */}
          <motion.a className="btn btn-primary" href="#start" whileTap={{ scale: 0.97 }}
                    transition={{ duration: 0.12, ease: EASE }}>
            Start tracing
          </motion.a>
          <a className="btn btn-ghost" href="#how">See a live trace</a>
        </div>
      </div>

      <div className="panel">
        <div className="panel-head">
          <span className="panel-title">path to <b>api.tracebound.io</b></span>
          <span className="dest">live . 6 hops</span>
        </div>
        <svg className="trace" viewBox="0 0 560 300" role="img"
             aria-label="A traceroute path forming across six hops, colored from low to high latency.">
          <defs>
            <linearGradient id="latency" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0" stopColor="var(--signal-fast)" />
              <stop offset="0.6" stopColor="var(--signal-mid)" />
              <stop offset="1" stopColor="var(--signal-slow)" />
            </linearGradient>
          </defs>
          <polyline className="route-path" points={POINTS} fill="none"
                    stroke="var(--line)" strokeWidth={2} />
          {/* stroke draw via pathLength: 1, animating dashoffset 1 -> 0 */}
          <motion.polyline
            points={POINTS} fill="none" stroke="url(#latency)" strokeWidth={2.5} strokeLinecap="round"
            initial={reduce ? false : { pathLength: 0 }}
            animate={{ pathLength: 1 }}
            transition={{ duration: 1.7, delay: 0.35, ease: EASE }}
          />
          {HOPS.map((h, i) => (
            <motion.circle
              key={i} cx={h.x} cy={h.y} r={i === HOPS.length - 1 ? 7 : 5} fill={hopColor(h.ms)}
              style={{ transformBox: "fill-box", transformOrigin: "center" }}
              initial={reduce ? false : { opacity: 0, scale: 0.5 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.42, delay: 0.35 + (i / (HOPS.length - 1)) * 1.7, ease: EASE }}
            />
          ))}
        </svg>
      </div>
    </section>
  );
}

// Scroll-reveal for the section below the fold: whileInView, once, no scroll listener, no useState.
export function Signal() {
  const reveal = {
    initial: { opacity: 0, transform: "translateY(18px)" },
    whileInView: { opacity: 1, transform: "translateY(0px)" },
    viewport: { once: true, amount: 0.3 },
    transition: { duration: 0.6, ease: EASE },
  };
  return (
    <section className="signal" id="how">
      <motion.div {...reveal}>
        <div className="big-stat">1.9<span className="u">s to full path</span></div>
        <p className="big-cap">
          A trace resolves the whole route, DNS to destination, in under two seconds.
          You read the map while the packet is still in flight.
        </p>
      </motion.div>
      <div className="facts">
        <motion.div className="fact" {...reveal}>
          <div className="n">every hop</div>
          <div className="t">latency, ASN, org and geo on each node, not just the endpoint.</div>
        </motion.div>
        <motion.div className="fact" {...reveal} transition={{ ...reveal.transition, delay: 0.08 }}>
          <div className="n">slow hops, flagged</div>
          <div className="t">the amber leg is where the route bends. The color is the data, not decoration.</div>
        </motion.div>
      </div>
    </section>
  );
}
