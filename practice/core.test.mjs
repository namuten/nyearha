import test from "node:test";
import assert from "node:assert/strict";
import { noteIndexAt, nextPlayedIndex, keyChanges, solfege, loopBounds, beatMs } from "./core.js";

const N = [{ms:0,end:1000,rest:true},{ms:1000,end:2000,pitch:"G3",rest:false},{ms:2000,end:3000,pitch:"A3",rest:false}];
test("before first / inside / at boundary", () => {
  assert.equal(noteIndexAt(N, -5), -1); assert.equal(noteIndexAt(N, 500), 0);
  assert.equal(noteIndexAt(N, 1000), 1); assert.equal(noteIndexAt(N, 9999), 2); });
test("next played skips rests", () => { assert.equal(nextPlayedIndex(N, 0), 1); assert.equal(nextPlayedIndex(N, 2), -1); });
test("key changes", () => assert.deepEqual(keyChanges(["L1","L2","L3"], ["L1","L2"]), {press: [], release: ["L3"]}));
test("key changes press and order", () =>
  assert.deepEqual(keyChanges(["L1"], ["R2","L1","R1"]), {press: ["R2","R1"], release: []}));
test("solfege", () => { assert.equal(solfege("G3"), "솔"); assert.equal(solfege("F#3"), "파♯"); assert.equal(solfege("Bb3"), "시♭"); assert.equal(solfege("C6"), "도"); });
test("loop to last measure ends at audio end", () =>
  assert.deepEqual(loopBounds([0, 4000, 8000], 14, 2, 3), {from: 4000, to: 14000}));
test("loop mid range", () =>
  assert.deepEqual(loopBounds([0, 4000, 8000], 14, 1, 2), {from: 0, to: 8000}));
test("beat ms honours rate", () => assert.equal(beatMs([0, 4000, 8000], 14, 4, 1, 0.5), 2000));
test("beat ms last measure", () => assert.equal(beatMs([0, 4000, 8000], 14, 4, 3, 1), 1500));
