// Astrology planet-in-sign influence text
// Keyed by language ('en' / 'uk'), then planet name, then zodiac index 0-11 (Aries … Pisces)
const ASTRO_PLANET_SIGN = {
  en: {
    Mercury: [
      "Sharp, direct mind. Quick decisions, competitive thinking. Enthusiasm for new ideas.",
      "Patient thinker, learns through the senses. Practical and thorough but can be stubborn in views.",
      "At home here — quick-witted, versatile, loves conversation. Tendency to scatter attention.",
      "Intuitive, emotionally driven thinking. Strong memory; logic coloured by feeling.",
      "Creative, expressive, proud in speech. Natural storyteller; can be dramatic in communication.",
      "Analytical and precise. Excellent at detail, criticism, and systematic problem-solving.",
      "Diplomatic, seeks balanced views. Weighs pros and cons; indecision possible.",
      "Probing, intense thought. Penetrating insight; keeps secrets, drawn to hidden matters.",
      "Expansive philosopher. Optimistic, broad-minded, love of travel and higher learning.",
      "Strategic and disciplined. Thinks long-term, values tradition and practical results.",
      "Original, rebellious ideas. Progressive thinking; humanitarian and unconventional.",
      "Imaginative, intuitive, sometimes vague. Absorbs impressions rather than analysing them.",
    ],
    Venus: [
      "Bold in love, direct pursuit. Excitement and novelty valued over security.",
      "Sensual, loyal, steadfast. Enjoys beauty, comfort, and lasting partnerships.",
      "Flirtatious and witty. Loves variety; needs intellectual connection in relationships.",
      "Nurturing, devoted, home-oriented. Emotional depth; family bonds are paramount.",
      "Warm, generous, loves grandly. Dramatic in romance; loyalty and admiration key.",
      "Refined, modest, quality-focused. Nitpicky in love; values practical care and devotion.",
      "Harmonious, beauty-seeking. Natural charm; partnerships and fairness are central.",
      "Intense, transformative bonds. Deep desire and potential jealousy; all-or-nothing.",
      "Freedom-loving adventurer. Philosophical connection valued; resists possessiveness.",
      "Reserved, loyal, status-aware. Shows love through responsibility and long-term commitment.",
      "Unconventional, friendship-based. Values independence; drawn to progressive partners.",
      "Romantic, dreamy, self-sacrificing. Spiritual love; susceptible to idealisation.",
    ],
    Mars: [
      "Powerful, fearless, pioneering. Thrives on challenge; can be impulsive and combative.",
      "Slow to anger but unstoppable once aroused. Tenacious, practical, sensual drive.",
      "Active mind as drive; multitasks energetically. Variable stamina, debate-loving.",
      "Protective, moody energy. Motivated by security and family; indirect but persistent.",
      "Bold, creative, proud action. Natural leader; dramatic expression of willpower.",
      "Precise, hard-working drive. Motivated by improvement and effectiveness; self-critical.",
      "Driven toward fairness; can avoid direct confrontation. Social energy, strategic.",
      "Relentless, intense power. Magnetic sexuality; strategic and uncompromising.",
      "Enthusiastic, freedom-seeking action. Philosophical goals; loves adventure and risk.",
      "Disciplined, ambitious, patient. Long-range vision; persistent climb toward mastery.",
      "Erratic but inventive energy. Progressive rebelliousness; humanitarian goals.",
      "Elusive, sensitive, compassionate drive. Motivated by empathy; energy fluctuates.",
    ],
    Jupiter: [
      "Bold optimism, entrepreneurial spirit. Luck through courage and initiating new ventures.",
      "Abundance through persistence and tangible effort. Enjoys material security and nature.",
      "Expansive intellect, luck through communication. Benefits from teaching and learning.",
      "Growth through emotional nurturing. Home, family, and protective instincts are amplified.",
      "Generous, theatrical optimism. Luck through creativity, children, romance, performance.",
      "Growth via service and practical skill. Benefits from health, analysis, and diligent work.",
      "Expansion through diplomacy and partnership. Luck in relationships and the arts.",
      "Deep transformative growth. Luck through investigation, shared resources, psychology.",
      "At home here — broad wisdom and adventure. Luck through travel, philosophy, and teaching.",
      "Growth through ambition and structure. Success via discipline, career, and authority.",
      "Humanitarian expansion. Luck through groups, technology, and progressive ideals.",
      "Spiritual and artistic growth. Luck through compassion, imagination, and solitude.",
    ],
    Saturn: [
      "Discipline applied to new beginnings. Lessons in courage, independence, and patience.",
      "Rewards slow, steady material effort. Tests stubbornness; builds lasting resources.",
      "Mental discipline required. Communication structured but sometimes over-cautious.",
      "Emotional responsibility, family duty. Inner security must be earned through effort.",
      "Lessons in humility and creative discipline. Pride tested; long-term creative commitment.",
      "Exalted here — mastery through meticulous work. Health, routine, and precision rewarded.",
      "Challenges in relationships and fairness. Karmic partnerships; balance demanded.",
      "Intense karmic transformation. Control tested; deep psychological pruning.",
      "Restricts easy optimism; demands earned wisdom. Travel and philosophy require structure.",
      "At home here — authority through hard work. Career success via patience and integrity.",
      "Discipline applied to society and progress. Innovations tested for long-term value.",
      "Hidden restrictions, spiritual discipline. Isolation can be productive; escapism challenged.",
    ],
    Uranus: [
      "Sudden, energetic reinvention. Revolutionary impulse; breaks old patterns dramatically.",
      "Disrupts comfort and tradition. Change comes to material values and routines.",
      "Lightning-fast communication changes. Mental revolutions; technology and media.",
      "Upsets domestic norms. Unconventional family structures; emotional breakthroughs.",
      "Creative rebellion, dramatic originality. Genius in arts and self-expression.",
      "Revolutionises work and health. Sudden changed routines; innovative methodology.",
      "Disrupts social norms in partnerships. Progressive relationships; equality demanded.",
      "Deep psychological upheaval. Sudden power shifts; transformation of hidden structures.",
      "Liberates philosophy and travel. New world-views arrive suddenly; freedom from dogma.",
      "Breaks traditional authority. Career upheaval; institutions reimagined.",
      "At home here — collective awakening. Technology, human rights, radical innovation.",
      "Dissolves spiritual boundaries. Intuition amplified; dreams and imagination shaken.",
    ],
    Neptune: [
      "Mystical impulse drives action. Idealism in leadership; sacrifice for a vision.",
      "Spiritual connection to earth and senses. Dissolves materialism; artistic appreciation.",
      "Imagination in thought and speech. Inspiration, but confusion or deception possible.",
      "Heightened emotional intuition and empathy. Family idealism; spiritual home life.",
      "Romantic, artistic transcendence. Creative genius; risk of illusion in love.",
      "Idealistic service and healing. Dissolves boundaries of analysis; spiritual health.",
      "Idealises relationships and beauty. Romantic illusion common; longing for union.",
      "At home in depth and mystery. Powerful psychic undertow; intense spiritual renewal.",
      "Spiritual quest through travel and philosophy. Dissolves cultural boundaries.",
      "Dissolves authority and tradition. Spiritual career; structures erode slowly.",
      "Collective spiritual idealism. Humanitarian dreams; shared illusions.",
      "At home here — boundless imagination. Deep psychic sensitivity; compassionate transcendence.",
    ],
    Earth: [
      "Energetic, pioneering year. Bold actions bring results; impulsive decisions tempered.",
      "Grounding stability, productivity. Material achievements; sensory pleasures favoured.",
      "Busy, communicative period. Learning, short journeys, ideas flow freely.",
      "Emotional focus on home and roots. Intuition strong; nurture yourself and others.",
      "Creative spotlight. Romance, play, and self-expression bring fulfilment.",
      "Attention to health and detail. Productive routines; practical improvements rewarded.",
      "Social harmony emphasised. Relationships flourish; balance between self and others.",
      "Deep transformation. Hidden matters surface; personal power is tested and renewed.",
      "Expansive horizons. Travel, learning, and philosophy bring optimism.",
      "Ambition and discipline rewarded. Career achievements; long-term planning pays off.",
      "Innovation and group action. Progressive ideas; community and friendship highlighted.",
      "Intuition and imagination strong. Rest, creativity, and spiritual insight benefit.",
    ],
  },
  uk: {
    Mercury: [
      "Гострий, прямий розум. Швидкі рішення, конкурентне мислення. Ентузіазм до нових ідей.",
      "Терплячий мислитель, вчиться через відчуття. Практичний і ретельний, але може бути впертим.",
      "Як вдома — кмітливий, різносторонній, любить спілкування. Схильність розпорошувати увагу.",
      "Інтуїтивне, емоційно забарвлене мислення. Сильна пам'ять; логіка пронизана почуттям.",
      "Творчий, виразний, гордовитий у мові. Природний оповідач; схильний до драматизму.",
      "Аналітичний і точний. Чудово справляється з деталями, критикою та систематизацією.",
      "Дипломатичний, шукає збалансованих поглядів. Зважує «за» і «проти»; можлива нерішучість.",
      "Пронизливе інтенсивне мислення. Глибоке проникнення в суть; зберігає таємниці.",
      "Широкий філософський погляд. Оптимістичний, широкий кругозір; любить подорожі й навчання.",
      "Стратегічний і дисциплінований. Мислить на перспективу; цінує традицію і практичний результат.",
      "Оригінальні, бунтарські ідеї. Прогресивне мислення; гуманізм і нетрадиційність.",
      "Уявне, інтуїтивне, іноді нечітке. Вбирає враження, а не аналізує.",
    ],
    Venus: [
      "Сміливе, пряме кохання. Новизна й збудження понад стабільність.",
      "Чуттєва, вірна, стійка. Насолоджується красою, затишком і тривалими стосунками.",
      "Кокетлива й дотепна. Любить різноманітність; потрібен інтелектуальний зв'язок.",
      "Дбайлива, відданна, орієнтована на дім. Емоційна глибина; сім'я понад усе.",
      "Тепла, щедра, любить по-великому. Драматична у романтиці; лояльність і захоплення — ключові.",
      "Вишукана, скромна, орієнтована на якість. Прискіплива в коханні; практична турбота.",
      "Гармонійна, прагне краси. Природний шарм; партнерство і справедливість у центрі.",
      "Інтенсивні, трансформуючі зв'язки. Глибоке бажання і можлива ревнощі; все або нічого.",
      "Волелюбна пригодниця. Цінує філософський зв'язок; опирається власництву.",
      "Стримана, вірна, статусна. Виявляє любов через відповідальність і довгострокові зобов'язання.",
      "Нетрадиційна, базована на дружбі. Цінує незалежність; приваблює прогресивних партнерів.",
      "Романтична, мрійлива, самовіддана. Духовне кохання; схильна до ідеалізації.",
    ],
    Mars: [
      "Потужний, безстрашний, першопрохідець. Процвітає в умовах виклику; може бути імпульсивним.",
      "Повільно гніваться, але нестримний. Наполегливий, практичний, чуттєва енергія.",
      "Активний розум як рушій; енергійно виконує кілька справ. Мінлива витривалість.",
      "Захисна, мінлива енергія. Мотивований безпекою і сім'єю; непрямий, але наполегливий.",
      "Смілива, творча, горда дія. Природний лідер; яскравий вияв сили волі.",
      "Точний, працьовитий. Мотивований покращенням і ефективністю; самокритичний.",
      "Прагне справедливості; уникає прямого протистояння. Соціальна енергія, стратегічний.",
      "Невпинна, інтенсивна сила. Магнетична сексуальність; стратегічний і безкомпромісний.",
      "Ентузіастична, свободолюбна дія. Філософські цілі; любить пригоди й ризик.",
      "Дисциплінований, амбітний, терплячий. Далекосяжне бачення; наполегливий шлях до майстерності.",
      "Хаотична, але винахідлива енергія. Прогресивний бунт; гуманістичні цілі.",
      "Невловимий, чутливий, співчутливий рух. Мотивований емпатією; енергія коливається.",
    ],
    Jupiter: [
      "Сміливий оптимізм, підприємницький дух. Удача через хоробрість і нові починання.",
      "Достаток через наполегливість і реальні зусилля. Насолоджується матеріальною безпекою.",
      "Широкий інтелект, удача через спілкування. Вигода від навчання і викладання.",
      "Зростання через емоційну турботу. Дім, сім'я і захисні інстинкти посилюються.",
      "Щедрий, театральний оптимізм. Удача через творчість, дітей, романтику і виступи.",
      "Зростання через служіння і практичні навички. Здоров'я, аналіз і ретельна праця.",
      "Розширення через дипломатію і партнерство. Удача у стосунках і мистецтві.",
      "Глибоке трансформуюче зростання. Удача через дослідження, спільні ресурси, психологію.",
      "Як вдома — широка мудрість і пригоди. Удача через подорожі, філософію і навчання.",
      "Зростання через амбіції і структуру. Успіх завдяки дисципліні, кар'єрі й авторитету.",
      "Гуманістичне розширення. Удача через групи, технології та прогресивні ідеали.",
      "Духовне й художнє зростання. Удача через співчуття, уяву і усамітнення.",
    ],
    Saturn: [
      "Дисципліна на новому старті. Уроки хоробрості, незалежності і терпіння.",
      "Нагороджує повільні, стійкі матеріальні зусилля. Перевіряє впертість; будує ресурси.",
      "Потрібна розумова дисципліна. Спілкування структуроване, але іноді надто обережне.",
      "Емоційна відповідальність, сімейний обов'язок. Внутрішня безпека здобувається зусиллями.",
      "Уроки смиренності й творчої дисципліни. Гордість перевіряється; тривале творче зобов'язання.",
      "Екзальтований тут — майстерність через ретельну роботу. Здоров'я, рутина і точність.",
      "Виклики у стосунках і справедливості. Кармічні партнерства; вимагається баланс.",
      "Інтенсивна кармічна трансформація. Контроль перевіряється; глибоке психологічне очищення.",
      "Обмежує легкий оптимізм; вимагає здобутої мудрості. Подорожі й філософія потребують структури.",
      "Як вдома — авторитет через важку роботу. Кар'єрний успіх завдяки терпінню і доброчесності.",
      "Дисципліна заради суспільства і прогресу. Інновації перевіряються на довгострокову цінність.",
      "Приховані обмеження, духовна дисципліна. Усамітнення може бути продуктивним.",
    ],
    Uranus: [
      "Раптове, енергійне переродження. Революційний імпульс; різко ламає старі шаблони.",
      "Руйнує комфорт і традицію. Зміни торкаються матеріальних цінностей і рутини.",
      "Блискавичні зміни у комунікації. Розумові революції; технології й медіа.",
      "Порушує домашні норми. Нетрадиційні сімейні структури; емоційні прориви.",
      "Творчий бунт, яскрава оригінальність. Геніальність у мистецтві й самовираженні.",
      "Революціонізує роботу і здоров'я. Раптові зміни в рутині; інноваційні методи.",
      "Руйнує соціальні норми у партнерстві. Прогресивні стосунки; вимагається рівність.",
      "Глибоке психологічне потрясіння. Раптові зміни влади; трансформація прихованих структур.",
      "Визволяє філософію і подорожі. Нові світогляди з'являються раптово.",
      "Ламає традиційний авторитет. Кар'єрні потрясіння; інститути переосмислюються.",
      "Як вдома — колективне пробудження. Технології, права людини, радикальні інновації.",
      "Розчиняє духовні межі. Інтуїція посилюється; сни й уява струшуються.",
    ],
    Neptune: [
      "Містичний імпульс рухає дійсністю. Ідеалізм у лідерстві; жертва заради бачення.",
      "Духовний зв'язок із землею і відчуттями. Розчиняє матеріалізм; художнє сприйняття.",
      "Уява в думках і мові. Натхнення, але можлива плутанина чи обман.",
      "Підвищена емоційна інтуїція і емпатія. Сімейний ідеалізм; духовне домашнє життя.",
      "Романтична, художня трансцендентність. Творчий геній; ризик ілюзії в коханні.",
      "Ідеалістичне служіння і зцілення. Розчиняє межі аналізу; духовне здоров'я.",
      "Ідеалізує стосунки і красу. Романтична ілюзія; прагнення єднання.",
      "Як вдома у глибині й таємниці. Потужний психічний потяг; духовне оновлення.",
      "Духовний пошук через подорожі й філософію. Розчиняє культурні межі.",
      "Розчиняє авторитет і традицію. Духовна кар'єра; структури поступово руйнуються.",
      "Колективний духовний ідеалізм. Гуманістичні мрії; спільні ілюзії.",
      "Як вдома — безмежна уява. Глибока психічна чутливість; співчутлива трансцендентність.",
    ],
    Earth: [
      "Енергійний, першопрохідницький рік. Сміливі дії приносять результати.",
      "Стабільність і продуктивність. Матеріальні досягнення; задоволення чуттів.",
      "Насичений, комунікативний період. Навчання, короткі подорожі, ідеї вільно течуть.",
      "Емоційний фокус на домі й коренях. Інтуїція сильна; піклуйтеся про себе та інших.",
      "Творчий прожектор. Романтика, гра й самовираження приносять задоволення.",
      "Увага на здоров'ї й деталях. Продуктивна рутина; практичні покращення нагороджуються.",
      "Наголос на соціальній гармонії. Стосунки процвітають; баланс між собою і іншими.",
      "Глибока трансформація. Приховані речі виходять на поверхню; особиста сила перевіряється.",
      "Розширення горизонтів. Подорожі, навчання й філософія приносять оптимізм.",
      "Нагороджуються амбіції й дисципліна. Кар'єрні досягнення; довгострокове планування.",
      "Інновації й групові дії. Прогресивні ідеї; спільнота й дружба у центрі.",
      "Інтуїція й уява сильні. Відпочинок, творчість і духовне осяяння на користь.",
    ],
  },
};

// ─────────────────────────────────────────────────────────────────────────────
// WARP STARS  (animation state + render — references cv/ctx/state/draw from solar_system.html)
// ─────────────────────────────────────────────────────────────────────────────
let warpStars=null;
let warpAnimId=null;
let warpLastTime=null;

function buildWarpStars(){
  // Build from starsCache so the same dots the user sees as bg stars are animated
  if(!starsCache && cv) starsCache=buildStars(cv.width,cv.height);
  if(!starsCache) return [];
  const arr=[];
  const cx=cv.width/2, cy=cv.height/2;
  const maxR=Math.hypot(cx,cy);
  for(const s of starsCache){
    const dx=s.x-cx, dy=s.y-cy;
    const angle=Math.atan2(dy,dx);
    const dist=Math.max(0.02, Math.hypot(dx,dy)/maxR);
    const speed=0.003+Math.random()*0.006;
    arr.push({angle, dist, speed, r:s.r, g:s.g, b:s.b, a:s.a, size:s.s});
  }
  return arr;
}

function tickWarp(ts){
  if(!state.warpMode){ warpAnimId=null; warpLastTime=null; return; }
  const w=cv.width, h=cv.height;
  if(!w||!h){ warpAnimId=requestAnimationFrame(tickWarp); return; }
  if(warpLastTime===null) warpLastTime=ts;
  const dt=Math.min(ts-warpLastTime,80);
  warpLastTime=ts;

  // Rebuild warp particles if starsCache was rebuilt (e.g. settings changed)
  if(!warpStars||warpStars.length!==(starsCache||[]).length) warpStars=buildWarpStars();

  // Draw scene (static stars are suppressed inside draw() when warpMode is on)
  draw();

  // Overlay animated bg-star dots — slow outward drift from centre
  const cx=w/2, cy=h/2;
  const maxR=Math.hypot(cx,cy);
  const warpFactor=(state.warpSpeed||0.15);
  const starOp=state.starOpacity||1.0;
  ctx.save();
  for(const s of warpStars){
    s.dist+=s.speed*warpFactor*dt/16;
    if(s.dist>1.4){
      s.dist=0.005+Math.random()*0.02;
      s.speed=0.003+Math.random()*0.006;
      s.angle=Math.random()*Math.PI*2;
    }
    const r=s.dist*maxR;
    const sx=cx+r*Math.cos(s.angle);
    const sy=cy+r*Math.sin(s.angle);
    ctx.beginPath();
    ctx.arc(sx,sy,s.size,0,Math.PI*2);
    ctx.fillStyle=`rgba(${s.r},${s.g},${s.b},${Math.min(1,s.a/255*starOp).toFixed(2)})`;
    ctx.fill();
  }
  ctx.restore();

  warpAnimId=requestAnimationFrame(tickWarp);
}

// ─────────────────────────────────────────────────────────────────────────────
// NORTHERN CONSTELLATIONS
// Stars: [ra_hours, dec_degrees] — azimuthal equidistant projection from North Pole.
// Visible range: dec -30° to 90° (120° span).
// ─────────────────────────────────────────────────────────────────────────────
const CONSTELLATIONS_NORTH=[
  {name:'Ursa Major',color:'#a0d0ff',stars:[
    [11.062,61.75],[11.897,53.69],[12.257,57.03],[12.900,55.96],[13.398,54.93],[13.792,49.31],[13.524,49.01],
    [10.285,66.99],[9.849,59.04]
  ],lines:[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,3],[0,7],[7,8]]},
  {name:'Ursa Minor',color:'#80c8ff',stars:[
    [2.530,89.26],[14.845,74.16],[15.734,77.79],[16.292,75.76],[17.537,86.59],[16.766,82.04],[15.345,71.83]
  ],lines:[[0,4],[4,5],[5,1],[1,6],[6,2],[2,3],[3,0]]},
  {name:'Cassiopeia',color:'#ffb0d0',stars:[
    [0.675,56.54],[1.103,60.72],[0.945,60.72],[1.431,60.24],[0.153,59.15]
  ],lines:[[4,0],[0,1],[1,2],[2,3]]},
  {name:'Orion',color:'#ffd080',stars:[
    [5.242,-8.20],[5.533,-0.30],[5.919,7.41],[5.679,1.94],[5.581,-1.94],[5.796,-9.67],[6.127,14.21],
    [5.419,6.35]
  ],lines:[[0,1],[1,2],[2,3],[3,4],[4,5],[5,0],[1,7],[7,6],[6,2],[3,5]]},
  {name:'Perseus',color:'#d0b0ff',stars:[
    [3.405,49.86],[3.715,47.79],[3.080,53.51],[3.964,40.01],[4.115,50.36],[2.731,55.90]
  ],lines:[[5,2],[2,0],[0,1],[1,3],[3,4],[4,1],[0,4]]},
  {name:'Auriga',color:'#50e8a0',stars:[
    [5.278,45.99],[5.108,41.23],[5.992,54.29],[5.440,43.82],[6.002,44.95],[4.900,33.17]
  ],lines:[[0,1],[1,5],[5,3],[3,0],[0,2],[2,4],[4,0]]},
  {name:'Gemini',color:'#ffe060',stars:[
    [7.755,28.03],[7.585,31.89],[6.628,16.40],[6.754,12.90],[7.068,20.57],[7.301,21.98],
    [6.383,22.51],[6.247,22.51]
  ],lines:[[0,5],[5,4],[4,3],[3,2],[1,5],[1,6],[6,7],[7,2]]},
  {name:'Leo',color:'#ffa040',stars:[
    [10.140,11.97],[10.332,19.84],[9.879,23.77],[10.123,16.77],[11.818,14.57],[11.235,20.52],
    [9.764,26.01]
  ],lines:[[6,2],[2,1],[1,3],[3,0],[0,1],[0,4],[4,5],[5,1]]},
  {name:'Virgo',color:'#c8f080',stars:[
    [13.420,-11.16],[12.694,-1.45],[12.332,-0.67],[13.036,-5.54],[12.926,3.40],[13.578,0.59]
  ],lines:[[2,4],[4,1],[1,3],[3,0],[0,5],[5,3]]},
  {name:'Bootes',color:'#ff9060',stars:[
    [14.261,19.18],[14.750,27.07],[14.534,30.37],[14.686,16.42],[14.420,13.72],[13.911,18.40]
  ],lines:[[5,0],[0,4],[4,3],[3,0],[0,1],[1,2],[2,0]]},
  {name:'Corona Borealis',color:'#90d0ff',stars:[
    [15.578,26.71],[15.464,29.11],[15.712,26.30],[15.549,31.36],[15.702,28.27],[15.827,26.88]
  ],lines:[[3,1],[1,0],[0,4],[4,2],[2,5]]},
  {name:'Hercules',color:'#e080ff',stars:[
    [17.244,14.39],[16.503,21.49],[17.006,30.93],[16.714,31.60],[16.365,19.15],[17.394,37.15],
    [16.688,38.92],[17.657,46.01]
  ],lines:[[4,1],[1,0],[0,2],[2,3],[3,1],[3,6],[6,5],[5,7],[7,2]]},
  {name:'Lyra',color:'#80ffff',stars:[
    [18.615,38.78],[18.835,33.36],[18.908,36.90],[18.746,37.60],[18.913,39.67]
  ],lines:[[0,3],[3,2],[2,1],[1,4],[4,0],[3,4]]},
  {name:'Cygnus',color:'#b0e0ff',stars:[
    [20.691,45.28],[20.370,40.26],[19.495,27.96],[21.216,30.23],[19.938,35.08],[21.736,28.74]
  ],lines:[[0,1],[1,4],[4,2],[0,3],[3,5],[1,3]]},
  {name:'Aquila',color:'#ffc850',stars:[
    [19.846,8.87],[19.771,6.41],[19.677,10.61],[19.425,3.11],[20.189,0.82]
  ],lines:[[2,0],[0,1],[1,3],[0,4]]},
  {name:'Draco',color:'#90ffa0',stars:[
    [17.944,51.49],[17.507,52.30],[16.400,61.51],[15.415,58.97],[14.075,64.38],[12.558,69.79],
    [11.524,69.33],[17.146,65.71],[18.351,72.73],[17.694,68.79]
  ],lines:[[0,7],[7,8],[8,9],[9,1],[1,0],[1,2],[2,3],[3,4],[4,5],[5,6]]},
  {name:'Cepheus',color:'#d0a0ff',stars:[
    [22.829,70.56],[22.251,58.20],[23.656,77.63],[22.181,70.56],[21.310,62.59]
  ],lines:[[0,3],[3,2],[2,0],[0,1],[1,4],[4,3]]},
  {name:'Andromeda',color:'#ffb8a0',stars:[
    [0.140,29.09],[0.655,30.86],[1.162,35.62],[2.065,42.33],[23.063,42.33]
  ],lines:[[4,0],[0,1],[1,2],[2,3]]},
  {name:'Pegasus',color:'#ffd8b0',stars:[
    [0.140,29.09],[22.691,10.83],[21.744,9.87],[23.079,15.21],[23.063,28.08]
  ],lines:[[1,2],[2,3],[3,4],[4,0],[0,1]]},
  {name:'Scorpius',color:'#ff7070',stars:[
    [16.490,-26.43],[16.006,-22.62],[16.352,-25.60],[16.836,-34.29],[17.144,-43.24],
    [17.622,-42.99],[17.708,-39.03],[17.560,-37.10]
  ],lines:[[1,0],[0,2],[2,3],[3,4],[4,5],[5,6],[6,7]]}
];

// Project RA/Dec to canvas XY aligned with the zodiac sectors.
// RA 0h = Aries = right side of canvas; RA increases counter-clockwise,
// matching the ecliptic-longitude convention used for planet drawing.
// dec=90 -> centre, dec=-30 -> edge (120° span = min(w,h)*0.48*scale).
function projectStarToCanvas(ra_h, dec_deg, w, h, scale){
  const maxR=Math.min(w,h)*0.48*(scale||1.0);
  const r=(90-dec_deg)/120*maxR;
  const angle=ra_h*15*Math.PI/180;
  return {x:w/2+r*Math.cos(angle), y:h/2-r*Math.sin(angle)};
}

function drawConstellations(w, h, mouseX, mouseY){
  const sc=state.constScale||1.0;
  let hoveredConst=null;

  // Find hovered constellation
  if(mouseX!==null){
    outer:for(const c of CONSTELLATIONS_NORTH){
      for(const [ra,dec] of c.stars){
        const {x,y}=projectStarToCanvas(ra,dec,w,h,sc);
        if(Math.hypot(mouseX-x,mouseY-y)<20){hoveredConst=c.name;break outer;}
      }
    }
  }

  ctx.save();
  for(const c of CONSTELLATIONS_NORTH){
    const isHovered=(c.name===hoveredConst);
    const pts=c.stars.map(([ra,dec])=>projectStarToCanvas(ra,dec,w,h,sc));
    const {r,g,b}=hexToRgb(c.color);
    const lineAlpha=isHovered?0.88:0.28;
    const starAlpha=isHovered?1.0:0.55;

    // Lines
    ctx.strokeStyle=`rgba(${r},${g},${b},${lineAlpha})`;
    ctx.lineWidth=isHovered?1.8:0.9;
    ctx.setLineDash(isHovered?[]:[3,4]);
    for(const [ai,bi] of c.lines){
      if(ai>=pts.length||bi>=pts.length) continue;
      ctx.beginPath();
      ctx.moveTo(pts[ai].x,pts[ai].y);
      ctx.lineTo(pts[bi].x,pts[bi].y);
      ctx.stroke();
    }
    ctx.setLineDash([]);

    // Stars
    for(const p of pts){
      ctx.beginPath();
      ctx.arc(p.x,p.y,isHovered?3.5:2.0,0,Math.PI*2);
      ctx.fillStyle=`rgba(${r},${g},${b},${starAlpha})`;
      ctx.fill();
      if(isHovered){
        ctx.strokeStyle='rgba(255,255,255,0.6)';
        ctx.lineWidth=0.8;
        ctx.stroke();
      }
    }

    // Name label on hover
    if(isHovered){
      let cx2=0,cy2=0;
      for(const p of pts){cx2+=p.x;cy2+=p.y;}
      cx2/=pts.length; cy2/=pts.length;
      const txt=c.name;
      ctx.font="bold 13px 'Segoe UI',Arial";
      ctx.textAlign='center';
      ctx.textBaseline='bottom';
      ctx.fillStyle='rgba(0,0,0,0.75)';
      ctx.fillText(txt,cx2+1,cy2-6);
      ctx.fillStyle=`rgba(${r},${g},${b},1)`;
      ctx.fillText(txt,cx2,cy2-7);
    }
  }
  ctx.restore();
}

let constMouseX=null, constMouseY=null;
