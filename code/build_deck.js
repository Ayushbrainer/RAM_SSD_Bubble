const fs = require('fs');
const path = require('path');
const pptxgen = require('pptxgenjs');
// Run from the repo root: node code/build_deck.js  (needs: npm install pptxgenjs)
let applyTheme = null; try { ({ applyTheme } = require('./apply_theme.js')); } catch (e) { /* optional: writes theme colours */ }

const ROOT = path.join(__dirname, '..');
const CLIPS = ROOT + '/clips/';
const POSTERS = ROOT + '/code/posters/';  // optional first-frame posters (ffmpeg -i clip.mp4 -frames:v 1 poster.png)
const OUT = process.argv[2] || ROOT + '/RAM_AI_Bubble.pptx';
const narr = JSON.parse(fs.readFileSync(ROOT + '/code/narration.json', 'utf8'));

const THEME = {
  name: 'Memory Surge',
  headFontFace: 'Arial',
  bodyFontFace: 'Calibri',
  colors: {
    dk1: '0B0B0B', lt1: 'FFFFFF', dk2: '17202B', lt2: 'F4F4F1',
    accent1: '2A78D6', accent2: 'EB6834', accent3: '1BAF7A', accent4: 'EDA100', accent5: 'E87BA4', accent6: '52514E',
    hlink: '2A78D6', folHlink: '4A3AA7',
  },
};

const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9'; // 10 x 5.625 in, same 16:9 as the clips
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = 'The 2026 Memory Price Surge and the AI Bubble';
pres.author = 'Ayush Bhatt & Bu Dinglin';
const C = pres.SchemeColor;

// ---------------- layouts
pres.defineSlideMaster({
  title: 'TITLE_DARK', background: { color: THEME.colors.dk2 },
  objects: [
    { placeholder: { options: { name: 'title', type: 'title', x: 0.6, y: 1.25, w: 5.6, h: 1.7, fontSize: 34, bold: true, color: C.background1, valign: 'bottom', align: 'left', margin: 0 }, text: 'Title' } },
    { placeholder: { options: { name: 'body', type: 'body', x: 0.6, y: 3.1, w: 5.4, h: 0.9, fontSize: 16, color: 'C9D3DF', valign: 'top', align: 'left', margin: 0 }, text: 'Subtitle' } },
  ],
});
pres.defineSlideMaster({ title: 'CLIP', background: { color: 'FCFCFB' } });
pres.defineSlideMaster({
  title: 'END_DARK', background: { color: THEME.colors.dk2 },
  objects: [
    { placeholder: { options: { name: 'title', type: 'title', x: 0.6, y: 0.45, w: 8.8, h: 0.9, fontSize: 30, bold: true, color: C.background1, valign: 'top', align: 'left', margin: 0 }, text: 'Title' } },
  ],
});
pres.defineSlideMaster({
  title: 'SOURCES', background: { color: 'FFFFFF' },
  objects: [
    { placeholder: { options: { name: 'title', type: 'title', x: 0.6, y: 0.4, w: 8.8, h: 0.6, fontSize: 28, bold: true, color: C.text1, valign: 'top', align: 'left', margin: 0 }, text: 'Title' } },
  ],
  slideNumber: { x: 9.2, y: 5.2, w: 0.4, h: 0.25, fontSize: 10, color: '898781' },
});

const notesFor = (s) => `${s.speaker.toUpperCase()} | ${s.scene} | target ${s.time}\n\n${s.text}`;

// ---------------- 1. title
pres.addSection({ title: 'Opening' });
let sl = pres.addSlide({ masterName: 'TITLE_DARK', sectionTitle: 'Opening' });
sl.addText('The 2026 Memory Price Surge and the AI Bubble', { placeholder: 'title' });
sl.addText('How AI spending pushed memory prices up, and whether it is a bubble', { placeholder: 'body' });
sl.addText([{ text: 'Ayush Bhatt (G2610412E)  ·  Bu Dinglin (G2609929D)', options: { breakLine: true } },
            { text: 'Group 04  ·  Data Visualisation, NTU CCDS' }], {
  x: 0.6, y: 4.5, w: 5.6, h: 0.6, fontSize: 12, color: '9AA8B8', margin: 0, isTextBox: true, objectName: 'Byline' });
// motif: the real DDR4 price series as a quiet native line chart
const csv = fs.readFileSync(ROOT + '/data/ddr4_contract_price.csv', 'utf8').trim().split('\n').slice(1).map(l => l.split(','));
sl.addChart(pres.charts.LINE, [{ name: 'DDR4 8Gb contract price (USD)', labels: csv.map(r => r[0]), values: csv.map(r => +r[1]) }], {
  x: 6.3, y: 1.0, w: 3.3, h: 3.1, chartColors: [THEME.colors.accent2], lineSize: 3, lineDataSymbol: 'circle', lineDataSymbolSize: 5,
  catAxisHidden: true, valAxisHidden: true, valGridLine: { style: 'none' }, catGridLine: { style: 'none' }, showLegend: false,
  showTitle: false, objectName: 'DDR4 price motif',
});
sl.addText([{ text: '20×', options: { fontSize: 40, bold: true, color: THEME.colors.accent2, breakLine: true } },
            { text: 'memory chip price vs its 2023 low', options: { fontSize: 12, color: '9AA8B8' } }],
  { x: 6.4, y: 4.15, w: 3.2, h: 0.95, margin: 0, isTextBox: true, objectName: 'Headline stat' });
sl.addNotes(notesFor(narr.find(s => s.slide === 'title')));

// ---------------- clip slides
const sectionOf = { '01_hook_ram_kit': 'The surge', '06_consumer_impact': 'Who pays, who wins', '08_capex_projection': 'The bubble question' };
let section = null;
for (const s of narr) {
  if (s.slide !== 'clip') continue;
  if (sectionOf[s.clip]) { section = sectionOf[s.clip]; pres.addSection({ title: section }); }
  const slide = pres.addSlide({ masterName: 'CLIP', sectionTitle: section });
  const posterFile = POSTERS + s.clip + '.png';
  const media = { type: 'video', path: CLIPS + s.clip + '.mp4', x: 0, y: 0, w: 10, h: 5.625, objectName: 'Clip ' + s.clip };
  if (fs.existsSync(posterFile)) media.cover = 'data:image/png;base64,' + fs.readFileSync(posterFile).toString('base64');
  slide.addMedia(media);
  slide.addNotes(notesFor(s));
}

// ---------------- conclusion
pres.addSection({ title: 'Close' });
sl = pres.addSlide({ masterName: 'END_DARK', sectionTitle: 'Close' });
sl.addText('A scoreboard for the AI boom', { placeholder: 'title' });
const stats = [
  ['3.7×', 'Big Tech capex per quarter,', 'Q1 2022 to Q4 2025', THEME.colors.accent2],
  ['20×', 'DDR4 chip contract price,', 'Sep 2026 vs 2023 low', THEME.colors.accent1],
  ['76%', 'SK hynix operating margin,', '2Q26 (after 2023 losses)', THEME.colors.accent3],
];
stats.forEach(([big, l1, l2, col], i) => {
  const x = 0.6 + i * 3.0;
  sl.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.55, w: 2.75, h: 2.15, rectRadius: 0.08, fill: { color: '222D3A' },
                                              line: { color: '2E3B4B', width: 1 }, objectName: 'Stat card ' + (i + 1) });
  sl.addText(big, { x: x + 0.25, y: 1.75, w: 2.3, h: 0.95, fontSize: 48, bold: true, color: col, margin: 0, isTextBox: true, objectName: 'Stat ' + (i + 1) });
  sl.addText([{ text: l1, options: { breakLine: true } }, { text: l2 }],
    { x: x + 0.25, y: 2.75, w: 2.3, h: 0.75, fontSize: 14, color: 'C9D3DF', margin: 0, valign: 'top', isTextBox: true, objectName: 'Stat label ' + (i + 1) });
});
sl.addText('AI demand is real, but the build-out may be ahead of revenue: expect write-downs and a slowdown, not a crash. If AI spending slows, memory prices could fall as fast as they rose.',
  { x: 0.6, y: 4.0, w: 8.8, h: 0.9, fontSize: 16, color: C.background1, margin: 0, valign: 'top', isTextBox: true, objectName: 'Takeaway' });
sl.addNotes(notesFor(narr.find(s => s.slide === 'conclusion')));

// ---------------- sources
sl = pres.addSlide({ masterName: 'SOURCES', sectionTitle: 'Close' });
sl.addText('Data and sources', { placeholder: 'title' });
const colA = [
  ['Datasets we compiled', true],
  ['DDR4 8Gb contract price, monthly, Jan 2022 to Sep 2026: DRAMeXchange via Silicon Analysts', false],
  ['Hyperscaler capex, quarterly, 2022 to 2025: Epoch AI, from company SEC filings', false],
  ['SK hynix operating profit, quarterly, 4Q22 to 2Q26: company results releases', false],
  ['Events on the price chart', true],
  ['DDR4 phase-out: TrendForce, 9 Jul 2025', false],
  ['RTX 50 supply cut (reported): Windows Central, 17 Dec 2025; Nvidia response via Tom\'s Guide, 22 Jan 2026', false],
];
const colB = [
  ['Other figures', true],
  ['Prices and market share: TrendForce; The Korea Times; Tom\'s Hardware via Tech-Insider', false],
  ['PC and phone impact: Gartner; Counterpoint Research via InfotechLead', false],
  ['Capex outlook: UBS via 24/7 Wall St. / Yahoo Finance', false],
  ['Bubble debate: Morgan Stanley via Benzinga; IoT Analytics', false],
  ['Full references with links are in the project report.', false],
];
const runs = (col) => col.map(([t, head], i) => ({ text: t, options: head
  ? { bold: true, fontSize: 14, color: THEME.colors.accent1, breakLine: i < col.length - 1, paraSpaceBefore: i ? 8 : 0 }
  : { fontSize: 12, color: '33302B', bullet: true, breakLine: i < col.length - 1, paraSpaceAfter: 3 } }));
sl.addText(runs(colA), { x: 0.6, y: 1.2, w: 4.3, h: 3.9, valign: 'top', margin: 0, isTextBox: true, objectName: 'Sources left' });
sl.addText(runs(colB), { x: 5.2, y: 1.2, w: 4.2, h: 3.9, valign: 'top', margin: 0, isTextBox: true, objectName: 'Sources right' });
sl.addNotes('(Not narrated. Leave on screen for about 3 seconds at the end of the recording, or cut it from the video.)');

(async () => {
  await pres.writeFile({ fileName: OUT });
  if (applyTheme) await applyTheme(OUT, THEME);
  console.log('wrote', OUT);
})();
