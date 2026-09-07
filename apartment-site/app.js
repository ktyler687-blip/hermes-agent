/* ─── DATA ─── */
const LISTINGS = [
  {
    id: 1, price: 2850, type: 'apartment', city: 'New York',
    address: '245 W 72nd St, Apt 8B', neighborhood: 'Upper West Side',
    beds: 2, baths: 1, sqft: 920, daysOnMarket: 3,
    badge: 'new', featured: true,
    amenities: ['pet', 'gym', 'laundry'],
    images: [
      'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&q=80',
      'https://images.unsplash.com/photo-1560448204-603b3fc33ddc?w=600&q=80',
      'https://images.unsplash.com/photo-1484154218962-a197022b5858?w=600&q=80',
      'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600&q=80',
    ],
    description: 'Stunning renovated 2-bedroom on the Upper West Side. Hardwood floors throughout, a chef\'s kitchen with quartz countertops, and a private balcony with Central Park views. 24-hour doorman, rooftop deck, and a state-of-the-art fitness center in the building.',
    agent: { name: 'Sarah Chen', title: 'Licensed Agent · Haven', rating: 4.9, reviews: 128, avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&q=80' },
    mapPos: { x: 28, y: 22 },
  },
  {
    id: 2, price: 1750, type: 'apartment', city: 'New York',
    address: '88 Fulton St, Apt 12', neighborhood: 'Financial District',
    beds: 1, baths: 1, sqft: 650, daysOnMarket: 7,
    badge: null, featured: true,
    amenities: ['gym', 'parking', 'pool'],
    images: [
      'https://images.unsplash.com/photo-1536376072261-38c75010e6c9?w=800&q=80',
      'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=600&q=80',
      'https://images.unsplash.com/photo-1565183928294-7063f23ce0f8?w=600&q=80',
    ],
    description: 'Modern 1-bedroom in the heart of the Financial District. Floor-to-ceiling windows with breathtaking city skyline views, an open-concept kitchen island, rooftop pool, concierge, and private parking garage.',
    agent: { name: 'James Park', title: 'Senior Agent · Haven', rating: 4.7, reviews: 92, avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&q=80' },
    mapPos: { x: 55, y: 70 },
  },
  {
    id: 3, price: 4200, type: 'condo', city: 'New York',
    address: '1 Central Park W, Unit 34', neighborhood: 'Columbus Circle',
    beds: 3, baths: 2, sqft: 1480, daysOnMarket: 1,
    badge: 'hot', featured: true,
    amenities: ['pet', 'parking', 'gym', 'pool', 'laundry'],
    images: [
      'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800&q=80',
      'https://images.unsplash.com/photo-1565182999561-18d7dc61c393?w=600&q=80',
      'https://images.unsplash.com/photo-1556020685-ae41abfc9365?w=600&q=80',
      'https://images.unsplash.com/photo-1560185007-5f0bb1866cab?w=600&q=80',
    ],
    description: 'Exceptional luxury condo overlooking Central Park. A grand entrance foyer, Sub-Zero kitchen, formal dining, and a master suite with a spa-style bathroom. Full-service white-glove building on one of Manhattan\'s most prestigious addresses.',
    agent: { name: 'Mia Torres', title: 'Luxury Specialist · Haven', rating: 5.0, reviews: 214, avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&q=80' },
    mapPos: { x: 38, y: 30 },
  },
  {
    id: 4, price: 1350, type: 'apartment', city: 'Chicago',
    address: '2111 N Clark St, Apt 304', neighborhood: 'Lincoln Park',
    beds: 1, baths: 1, sqft: 710, daysOnMarket: 14,
    badge: 'drop', featured: false,
    amenities: ['pet', 'laundry'],
    images: [
      'https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=800&q=80',
      'https://images.unsplash.com/photo-1556228453-efd6c1ff04f6?w=600&q=80',
    ],
    description: 'Charming updated 1-bedroom in vibrant Lincoln Park. Exposed brick, original hardwood floors, and a sunny bay window. Steps from the lakefront trail, world-class dining, and the Lincoln Park Zoo. Price recently reduced.',
    agent: { name: 'Tyler Brooks', title: 'Licensed Agent · Haven', rating: 4.6, reviews: 57, avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&q=80' },
    mapPos: { x: 20, y: 45 },
  },
  {
    id: 5, price: 2100, type: 'condo', city: 'Chicago',
    address: '400 N Lake Shore Dr, Unit 1802', neighborhood: 'Streeterville',
    beds: 2, baths: 2, sqft: 1050, daysOnMarket: 5,
    badge: 'new', featured: false,
    amenities: ['gym', 'pool', 'parking', 'laundry'],
    images: [
      'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800&q=80',
      'https://images.unsplash.com/photo-1560185008-b033106af5c3?w=600&q=80',
      'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&q=80',
    ],
    description: 'Gorgeous lake-view condo in one of Chicago\'s most sought-after buildings. Bright open floor plan, in-unit washer/dryer, and a large private balcony facing Lake Michigan. Indoor pool, fitness center, and 24-hour security.',
    agent: { name: 'Sarah Chen', title: 'Licensed Agent · Haven', rating: 4.9, reviews: 128, avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&q=80' },
    mapPos: { x: 65, y: 38 },
  },
  {
    id: 6, price: 3600, type: 'house', city: 'Miami',
    address: '740 NE 13th Ave', neighborhood: 'Edgewater',
    beds: 3, baths: 2, sqft: 1650, daysOnMarket: 9,
    badge: null, featured: true,
    amenities: ['pet', 'parking', 'pool'],
    images: [
      'https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800&q=80',
      'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&q=80',
      'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=600&q=80',
    ],
    description: 'Stunning modern home in Edgewater with Biscayne Bay views. Open-concept living, high ceilings, impact windows, and a resort-style backyard with heated pool and summer kitchen. Smart home tech and solar panels included.',
    agent: { name: 'Mia Torres', title: 'Luxury Specialist · Haven', rating: 5.0, reviews: 214, avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&q=80' },
    mapPos: { x: 45, y: 55 },
  },
  {
    id: 7, price: 1950, type: 'apartment', city: 'Los Angeles',
    address: '1412 S Figueroa St, Apt 201', neighborhood: 'South Park',
    beds: 1, baths: 1, sqft: 780, daysOnMarket: 2,
    badge: 'new', featured: false,
    amenities: ['gym', 'pool', 'parking'],
    images: [
      'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&q=80',
      'https://images.unsplash.com/photo-1565183928294-7063f23ce0f8?w=600&q=80',
    ],
    description: 'Sleek modern 1-bedroom in the heart of Downtown LA. High-end finishes, a designer kitchen, spa bathroom, and expansive city views. Walking distance to Staples Center, LA Live, and the city\'s best restaurants.',
    agent: { name: 'James Park', title: 'Senior Agent · Haven', rating: 4.7, reviews: 92, avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&q=80' },
    mapPos: { x: 30, y: 60 },
  },
  {
    id: 8, price: 3200, type: 'condo', city: 'Los Angeles',
    address: '888 S Olive St, Unit 1502', neighborhood: 'Bunker Hill',
    beds: 2, baths: 2, sqft: 1210, daysOnMarket: 4,
    badge: 'feat', featured: false,
    amenities: ['pet', 'gym', 'parking', 'pool', 'laundry'],
    images: [
      'https://images.unsplash.com/photo-1560184897-ae75f418493e?w=800&q=80',
      'https://images.unsplash.com/photo-1571508601891-ca5e7a713859?w=600&q=80',
      'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600&q=80',
    ],
    description: 'Exquisite high-rise condo with panoramic views of the LA skyline, mountains, and ocean. Gourmet kitchen, primary suite with wraparound terrace. Resort-style pool deck, wine cellar, screening room, and private dog park.',
    agent: { name: 'Tyler Brooks', title: 'Licensed Agent · Haven', rating: 4.6, reviews: 57, avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&q=80' },
    mapPos: { x: 72, y: 25 },
  },
  {
    id: 9, price: 2400, type: 'apartment', city: 'Seattle',
    address: '2001 8th Ave, Apt 15B', neighborhood: 'Belltown',
    beds: 2, baths: 1, sqft: 960, daysOnMarket: 6,
    badge: null, featured: false,
    amenities: ['pet', 'gym', 'laundry'],
    images: [
      'https://images.unsplash.com/photo-1484101403633-562f891dc89a?w=800&q=80',
      'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=600&q=80',
    ],
    description: 'Spacious 2-bedroom with Puget Sound and Olympic Mountain views. Polished concrete floors, a gourmet kitchen with waterfall island, and a private deck. Walkable to Pike Place Market from vibrant Belltown.',
    agent: { name: 'Sarah Chen', title: 'Licensed Agent · Haven', rating: 4.9, reviews: 128, avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&q=80' },
    mapPos: { x: 50, y: 40 },
  },
  {
    id: 10, price: 1600, type: 'apartment', city: 'Austin',
    address: '604 W 6th St, Unit 302', neighborhood: 'West 6th',
    beds: 1, baths: 1, sqft: 720, daysOnMarket: 11,
    badge: 'drop', featured: false,
    amenities: ['pet', 'gym', 'pool'],
    images: [
      'https://images.unsplash.com/photo-1560448204-603b3fc33ddc?w=800&q=80',
      'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=600&q=80',
    ],
    description: 'Hip 1-bedroom loft steps from Austin\'s legendary 6th Street. Industrial chic with exposed duct work and an oversized rooftop terrace. Price reduced — large dogs welcome. SXSW and ACL right outside your door.',
    agent: { name: 'James Park', title: 'Senior Agent · Haven', rating: 4.7, reviews: 92, avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&q=80' },
    mapPos: { x: 60, y: 65 },
  },
  {
    id: 11, price: 5500, type: 'condo', city: 'Miami',
    address: '1000 Brickell Plaza, PH 48', neighborhood: 'Brickell',
    beds: 3, baths: 3, sqft: 2100, daysOnMarket: 2,
    badge: 'hot', featured: false,
    amenities: ['pet', 'gym', 'parking', 'pool', 'laundry'],
    images: [
      'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&q=80',
      'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=600&q=80',
      'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=600&q=80',
    ],
    description: 'Extraordinary penthouse at the top of Brickell\'s most iconic tower. 12-foot ceilings, a private rooftop terrace with plunge pool, and 360° views of Biscayne Bay and the Miami skyline. Ultra-luxury amenities across five floors.',
    agent: { name: 'Mia Torres', title: 'Luxury Specialist · Haven', rating: 5.0, reviews: 214, avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&q=80' },
    mapPos: { x: 35, y: 75 },
  },
  {
    id: 12, price: 1100, type: 'apartment', city: 'Chicago',
    address: '3245 N Halsted St, Apt 2', neighborhood: 'Boystown',
    beds: 0, baths: 1, sqft: 480, daysOnMarket: 20,
    badge: null, featured: false,
    amenities: ['laundry'],
    images: [
      'https://images.unsplash.com/photo-1536376072261-38c75010e6c9?w=800&q=80',
    ],
    description: 'Cozy studio in the heart of Boystown. Recently updated with new appliances, fresh paint, and refinished hardwood floors. Coin laundry in building. Walk to the L, restaurants, shops, and Wrigley Field. Utilities included.',
    agent: { name: 'Tyler Brooks', title: 'Licensed Agent · Haven', rating: 4.6, reviews: 57, avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&q=80' },
    mapPos: { x: 80, y: 50 },
  },
  {
    id: 13, price: 2900, type: 'townhouse', city: 'Austin',
    address: '1805 E Cesar Chavez St', neighborhood: 'East Austin',
    beds: 3, baths: 2, sqft: 1380, daysOnMarket: 8,
    badge: 'new', featured: false,
    amenities: ['pet', 'parking', 'laundry'],
    images: [
      'https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800&q=80',
      'https://images.unsplash.com/photo-1480074568708-e7b720bb3f09?w=600&q=80',
    ],
    description: 'Modern townhouse in trendy East Austin. Private fenced yard, attached garage, and a rooftop deck. Chef\'s kitchen with quartz countertops and farmhouse sink. Walkable to breweries, coffee shops, and the famous Franklin Barbecue.',
    agent: { name: 'Sarah Chen', title: 'Licensed Agent · Haven', rating: 4.9, reviews: 128, avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&q=80' },
    mapPos: { x: 42, y: 58 },
  },
  {
    id: 14, price: 3800, type: 'house', city: 'Seattle',
    address: '4521 Phinney Ave N', neighborhood: 'Phinney Ridge',
    beds: 4, baths: 3, sqft: 2050, daysOnMarket: 3,
    badge: 'feat', featured: false,
    amenities: ['pet', 'parking', 'laundry'],
    images: [
      'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&q=80',
      'https://images.unsplash.com/photo-1575517111839-3a3843ee7f5d?w=600&q=80',
    ],
    description: 'Beautifully restored craftsman home on Phinney Ridge with sweeping Puget Sound views. Original character preserved with a new kitchen, master bath, and 200-amp electrical. Lush garden, detached 2-car garage, and mature trees.',
    agent: { name: 'James Park', title: 'Senior Agent · Haven', rating: 4.7, reviews: 92, avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&q=80' },
    mapPos: { x: 18, y: 32 },
  },
  {
    id: 15, price: 2300, type: 'apartment', city: 'Los Angeles',
    address: '5217 Hollywood Blvd, Apt 8', neighborhood: 'Hollywood',
    beds: 2, baths: 1, sqft: 875, daysOnMarket: 16,
    badge: 'drop', featured: false,
    amenities: ['pool', 'gym'],
    images: [
      'https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=800&q=80',
      'https://images.unsplash.com/photo-1560448204-603b3fc33ddc?w=600&q=80',
    ],
    description: 'Stylish mid-century 2-bedroom in the heart of Hollywood. Updated kitchen and baths, hardwood floors, and a private balcony. Resort-style pool and fitness center on site. Walking distance to the Walk of Fame. Price reduced.',
    agent: { name: 'Mia Torres', title: 'Luxury Specialist · Haven', rating: 5.0, reviews: 214, avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&q=80' },
    mapPos: { x: 68, y: 48 },
  },
  {
    id: 16, price: 4800, type: 'condo', city: 'New York',
    address: '56 Leonard St, Unit 22', neighborhood: 'Tribeca',
    beds: 3, baths: 2, sqft: 1720, daysOnMarket: 1,
    badge: 'hot', featured: false,
    amenities: ['pet', 'gym', 'parking', 'pool', 'laundry'],
    images: [
      'https://images.unsplash.com/photo-1560184897-ae75f418493e?w=800&q=80',
      'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=600&q=80',
      'https://images.unsplash.com/photo-1484154218962-a197022b5858?w=600&q=80',
    ],
    description: 'Magnificent Tribeca loft in the iconic Jenga Tower. Soaring ceilings, floor-to-ceiling windows with Hudson River views, custom millwork, and Wolf/Sub-Zero appliances. 75-foot pool, children\'s playroom, and private cinema.',
    agent: { name: 'Sarah Chen', title: 'Licensed Agent · Haven', rating: 4.9, reviews: 128, avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&q=80' },
    mapPos: { x: 48, y: 78 },
  },
];

/* ─── STATE ─── */
const state = {
  view: 'home',
  filtered: [...LISTINGS],
  page: 1,
  perPage: 8,
  cardView: 'grid',
  favorites: new Set(),
  cityFilter: '',
  typeFilter: '',
  filtersOpen: false,
};

/* ─── HELPERS ─── */
const fmt = n => '$' + n.toLocaleString();
const bedLabel = n => n === 0 ? 'Studio' : n === 1 ? '1 bed' : `${n} beds`;
const bedLabelShort = n => n === 0 ? 'Studio' : `${n} bd`;

/* ─── VIEW ROUTER ─── */
function showView(name) {
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  document.getElementById('view-' + name).classList.add('active');
  state.view = name;
  if (name === 'home') renderFeatured();
  if (name === 'listings') { applyFilters(); renderMapPins(); }
  window.scrollTo(0, 0);
}

/* ─── FEATURED ─── */
function renderFeatured() {
  const grid = document.getElementById('featured-grid');
  if (!grid) return;
  grid.innerHTML = LISTINGS.filter(l => l.featured).slice(0, 3).map(l => cardHTML(l)).join('');
}

/* ─── CARD HTML ─── */
function cardHTML(l, mode) {
  const isFav = state.favorites.has(l.id);
  const isListMode = mode === 'list';
  const badgeClass = { new: 'b-new', hot: 'b-hot', drop: 'b-drop', feat: 'b-feat' };
  const badgeText  = { new: 'New', hot: 'Hot', drop: 'Price Drop', feat: 'Featured' };
  const amenityLabel = { pet: 'Pets', gym: 'Gym', pool: 'Pool', parking: 'Parking', laundry: 'W/D' };

  return `<div class="card${isListMode ? ' lm' : ''}" onclick="openDetail(${l.id})">
    <div class="card-photo">
      <img src="${l.images[0]}" alt="${l.address}" loading="lazy"
           onerror="this.src='https://images.unsplash.com/photo-1486325212027-8081e485255e?w=600&q=80'" />
      ${l.badge ? `<span class="card-badge ${badgeClass[l.badge]}">${badgeText[l.badge]}</span>` : ''}
      <button class="card-save${isFav ? ' saved' : ''}" onclick="toggleFav(event,${l.id})" title="Save">
        <svg viewBox="0 0 24 24">
          <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
        </svg>
      </button>
      ${l.images.length > 1 ? `<span class="card-pcount">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5" fill="currentColor"/><polyline points="21 15 16 10 5 21"/></svg>
        ${l.images.length}
      </span>` : ''}
    </div>
    <div class="card-body">
      <div class="card-price">${fmt(l.price)}<span class="card-price-mo"> /mo</span></div>
      <div class="card-spec">
        ${bedLabelShort(l.beds)}<span class="spec-dot"></span>${l.baths} ba<span class="spec-dot"></span>${l.sqft.toLocaleString()} sqft
      </div>
      <div class="card-addr">${l.address}</div>
      <div class="card-nbhd">${l.neighborhood}, ${l.city}</div>
    </div>
    <div class="card-foot">
      <span class="card-age">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
        ${l.daysOnMarket}d ago
      </span>
      <div class="card-tags">
        ${l.amenities.slice(0, 3).map(a => `<span class="ctag">${amenityLabel[a]}</span>`).join('')}
      </div>
    </div>
  </div>`;
}

/* ─── FILTERS ─── */
function applyFilters() {
  const search  = (document.getElementById('ls-search')?.value || '').toLowerCase();
  const beds    = document.getElementById('filter-beds')?.value || '';
  const maxPrice= parseInt(document.getElementById('filter-price')?.value || '0');
  const type    = document.getElementById('filter-type')?.value || state.typeFilter || '';
  const baths   = parseInt(document.getElementById('filter-baths')?.value || '0');
  const sqftMin = parseInt(document.getElementById('filter-sqft-min')?.value || '0');
  const sqftMax = parseInt(document.getElementById('filter-sqft-max')?.value || '999999');
  const sortBy  = document.getElementById('filter-sort')?.value || 'newest';
  const pet     = document.getElementById('filter-pet')?.checked;
  const parking = document.getElementById('filter-parking')?.checked;
  const gym     = document.getElementById('filter-gym')?.checked;
  const pool    = document.getElementById('filter-pool')?.checked;
  const laundry = document.getElementById('filter-laundry')?.checked;

  let results = LISTINGS.filter(l => {
    if (search && !l.address.toLowerCase().includes(search) &&
        !l.city.toLowerCase().includes(search) &&
        !l.neighborhood.toLowerCase().includes(search)) return false;
    if (state.cityFilter && l.city !== state.cityFilter) return false;
    if (beds) {
      if (beds === 'studio' && l.beds !== 0) return false;
      else if (beds === '4' && l.beds < 4) return false;
      else if (beds !== 'studio' && beds !== '4' && l.beds !== parseInt(beds)) return false;
    }
    if (maxPrice && l.price > maxPrice) return false;
    if (type && l.type !== type) return false;
    if (baths && l.baths < baths) return false;
    if (l.sqft < sqftMin || l.sqft > sqftMax) return false;
    if (pet && !l.amenities.includes('pet')) return false;
    if (parking && !l.amenities.includes('parking')) return false;
    if (gym && !l.amenities.includes('gym')) return false;
    if (pool && !l.amenities.includes('pool')) return false;
    if (laundry && !l.amenities.includes('laundry')) return false;
    return true;
  });

  results.sort((a, b) => {
    if (sortBy === 'price-asc')  return a.price - b.price;
    if (sortBy === 'price-desc') return b.price - a.price;
    if (sortBy === 'sqft')       return b.sqft - a.sqft;
    return a.daysOnMarket - b.daysOnMarket;
  });

  state.filtered = results;
  state.page = 1;
  renderListings();
  renderMapPins();
}

function filterByCity(city) {
  state.cityFilter = city;
  showView('listings');
}
function filterByType(t) {
  state.typeFilter = t;
  showView('listings');
}
function doHeroSearch() {
  const val = document.getElementById('hero-input')?.value;
  const si  = document.getElementById('ls-search');
  if (val && si) si.value = val;
  showView('listings');
}
function clearFilters() {
  state.cityFilter = '';
  state.typeFilter = '';
  ['filter-beds','filter-price','filter-type','filter-baths','filter-sqft-min','filter-sqft-max'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = '';
  });
  ['filter-pet','filter-parking','filter-gym','filter-pool','filter-laundry'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.checked = false;
  });
  const si = document.getElementById('ls-search');
  if (si) si.value = '';
  applyFilters();
}

/* ─── RENDER LISTINGS ─── */
function renderListings() {
  const grid  = document.getElementById('ls-grid');
  const count = document.getElementById('ls-count');
  if (!grid) return;

  const total = state.filtered.length;
  const start = (state.page - 1) * state.perPage;
  const page  = state.filtered.slice(start, start + state.perPage);
  const mode  = state.cardView;

  count.textContent = `${total} home${total !== 1 ? 's' : ''}`;
  grid.className = 'ls-grid' + (mode === 'list' ? ' list-mode' : '');

  grid.innerHTML = page.length
    ? page.map(l => cardHTML(l, mode)).join('')
    : `<div class="ls-empty">
        <p>No homes match your current filters.</p>
        <a onclick="clearFilters();return false;">Clear all filters →</a>
      </div>`;

  renderPager(total);
}

function renderPager(total) {
  const pager = document.getElementById('ls-pager');
  if (!pager) return;
  const pages = Math.ceil(total / state.perPage);
  if (pages <= 1) { pager.innerHTML = ''; return; }

  let html = '';
  if (state.page > 1) html += `<button class="pg-btn" onclick="goPage(${state.page - 1})">‹</button>`;
  for (let i = 1; i <= pages; i++) {
    if (i === 1 || i === pages || Math.abs(i - state.page) <= 1)
      html += `<button class="pg-btn${i === state.page ? ' cur' : ''}" onclick="goPage(${i})">${i}</button>`;
    else if (Math.abs(i - state.page) === 2)
      html += `<span class="pg-btn dots">…</span>`;
  }
  if (state.page < pages) html += `<button class="pg-btn" onclick="goPage(${state.page + 1})">›</button>`;
  pager.innerHTML = html;
}

function goPage(p) {
  state.page = p;
  renderListings();
  document.getElementById('ls-panel')?.scrollTo({ top: 0, behavior: 'smooth' });
}

function setCardView(v) {
  state.cardView = v;
  document.getElementById('btn-grid').classList.toggle('active', v === 'grid');
  document.getElementById('btn-list').classList.toggle('active', v === 'list');
  renderListings();
}

function toggleFilters() {
  state.filtersOpen = !state.filtersOpen;
  document.getElementById('extra-filters').style.display = state.filtersOpen ? 'block' : 'none';
  document.getElementById('btn-more').classList.toggle('open', state.filtersOpen);
}

/* ─── FAVORITES ─── */
function toggleFav(e, id) {
  e.stopPropagation();
  if (state.favorites.has(id)) {
    state.favorites.delete(id);
    showToast('Removed from saved homes');
  } else {
    state.favorites.add(id);
    showToast('Saved ♥');
  }
  renderListings();
  if (state.view === 'home') renderFeatured();
}

/* ─── MAP PINS ─── */
function renderMapPins() {
  const container = document.getElementById('map-pins');
  if (!container) return;
  const start = (state.page - 1) * state.perPage;
  const page  = state.filtered.slice(start, start + state.perPage);
  container.innerHTML = page.map(l => `
    <div class="pin" style="left:${l.mapPos.x}%;top:${l.mapPos.y}%" onclick="openDetail(${l.id})">
      <div class="pin-lbl">${fmt(l.price)}</div>
      <div class="pin-tip">
        <strong>${fmt(l.price)}/mo</strong>
        <span>${bedLabel(l.beds)} · ${l.sqft.toLocaleString()} sqft<br>${l.neighborhood}</span>
      </div>
    </div>`).join('');
}

function toggleMap() {
  const map  = document.getElementById('ls-map');
  const lbl  = document.getElementById('map-toggle-label');
  const hidden = map.style.display === 'none';
  map.style.display = hidden ? '' : 'none';
  lbl.textContent = hidden ? 'Hide map' : 'Show map';
}

/* ─── DETAIL VIEW ─── */
function openDetail(id) {
  const l = LISTINGS.find(x => x.id === id);
  if (!l) return;

  const isFav = state.favorites.has(l.id);
  const amenityMeta = {
    pet:     ['<path d="M12 9c1.5 0 2.75 1.12 2.75 2.5S13.5 14 12 14s-2.75-1.12-2.75-2.5S10.5 9 12 9z"/><path d="M5.5 6c.83 0 1.5.67 1.5 1.5S6.33 9 5.5 9 4 8.33 4 7.5 4.67 6 5.5 6z"/><path d="M18.5 6c.83 0 1.5.67 1.5 1.5S19.33 9 18.5 9 17 8.33 17 7.5 17.67 6 18.5 6z"/><path d="M5.5 15c.83 0 1.5.67 1.5 1.5S6.33 18 5.5 18 4 17.33 4 16.5 4.67 15 5.5 15z"/><path d="M18.5 15c.83 0 1.5.67 1.5 1.5S19.33 18 18.5 18 17 17.33 17 16.5 17.67 15 18.5 15z"/>', 'Pet Friendly'],
    gym:     ['<path d="M6.5 6.5h11M6.5 17.5h11M6.5 6.5v11M17.5 6.5v11"/><path d="M3 12h3M18 12h3"/>', 'Fitness Center'],
    pool:    ['<path d="M2 12h20"/><path d="M2 17c1.5 0 2.5-1 4-1s2.5 1 4 1 2.5-1 4-1 2.5 1 4 1"/><path d="M2 7c1.5 0 2.5 1 4 1s2.5-1 4-1 2.5 1 4 1 2.5-1 4-1"/>', 'Swimming Pool'],
    parking: ['<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 17V7h4a3 3 0 0 1 0 6H9"/>', 'Parking'],
    laundry: ['<rect x="2" y="4" width="20" height="20" rx="2"/><circle cx="12" cy="14" r="4"/><path d="M7 8h.01M10 8h.01"/>', 'In-Unit Laundry'],
  };
  const bedIcon = '<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>';
  const bathIcon = '<path d="M4 12h16v6a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-6z"/><path d="M4 12V5a2 2 0 0 1 2-2h3v5"/>';
  const sqftIcon = '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/>';

  const featureItems = [
    [bedIcon,  bedLabel(l.beds)],
    [bathIcon, `${l.baths} Bathroom${l.baths > 1 ? 's' : ''}`],
    [sqftIcon, `${l.sqft.toLocaleString()} sq ft`],
    ...l.amenities.map(a => amenityMeta[a] || null).filter(Boolean),
  ];

  const thumbsHTML = l.images.slice(0, 4).map((img, i) =>
    `<div class="detail-thumb${i === 0 ? ' active' : ''}" onclick="switchThumb(this,'${img}')">
      <img src="${img}" alt="" />
    </div>`
  ).join('') + (l.images.length > 4 ? `<div class="detail-more-thumb">+${l.images.length - 4} more</div>` : '');

  const root = document.getElementById('detail-root');
  root.innerHTML = `
    <div class="detail-wrap">
      <button class="detail-back" onclick="showView('listings')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg>
        Back to listings
      </button>

      <img id="detail-hero" class="detail-hero-img" src="${l.images[0]}" alt="${l.address}"
           onerror="this.src='https://images.unsplash.com/photo-1486325212027-8081e485255e?w=800&q=80'" />

      <div class="detail-thumbs">${thumbsHTML}</div>

      <div class="detail-cols">
        <div class="detail-main">
          <div class="detail-row1">
            <div>
              <div class="detail-price">${fmt(l.price)}<em> /mo</em></div>
            </div>
            <div class="detail-acts">
              <button class="dact" onclick="toggleFavDetail(${l.id},this)" title="Save">
                <svg viewBox="0 0 24 24" fill="${isFav ? '#B84A2E' : 'none'}" stroke="${isFav ? '#B84A2E' : 'currentColor'}" stroke-width="1.6">
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
                </svg>
              </button>
              <button class="dact" onclick="showToast('Link copied!')" title="Share">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
              </button>
            </div>
          </div>
          <div class="detail-addr">${l.address} · ${l.neighborhood}, ${l.city}</div>

          <div class="detail-stats">
            <div class="dstat"><strong>${l.beds === 0 ? '—' : l.beds}</strong><span>${l.beds === 0 ? 'Studio' : 'Beds'}</span></div>
            <div class="dstat"><strong>${l.baths}</strong><span>Baths</span></div>
            <div class="dstat"><strong>${l.sqft.toLocaleString()}</strong><span>Sq Ft</span></div>
            <div class="dstat"><strong>${l.daysOnMarket}d</strong><span>On Market</span></div>
            <div class="dstat"><strong>${l.type.charAt(0).toUpperCase() + l.type.slice(1)}</strong><span>Type</span></div>
          </div>

          <div class="detail-sec">
            <h3>About this home</h3>
            <p class="detail-desc">${l.description}</p>
          </div>

          <div class="detail-sec">
            <h3>Features &amp; amenities</h3>
            <div class="feats-list">
              ${featureItems.map(([icon, label]) => `
                <div class="feat">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">${icon}</svg>
                  ${label}
                </div>`).join('')}
            </div>
          </div>

          <div class="detail-sec">
            <h3>Location</h3>
            <div class="detail-map-prev">
              <svg viewBox="0 0 420 180" preserveAspectRatio="xMidYMid slice">
                <rect class="mg" width="420" height="180"/>
                <rect class="mr" x="0" y="70" width="420" height="7"/>
                <rect class="mr" x="0" y="125" width="420" height="5"/>
                <rect class="mr" x="130" y="0" width="7" height="180"/>
                <rect class="mr" x="280" y="0" width="5" height="180"/>
                <rect class="mb" x="8" y="8" width="115" height="55" rx="2"/>
                <rect class="mbb" x="143" y="8" width="130" height="55" rx="2"/>
                <rect class="mb" x="290" y="8" width="122" height="55" rx="2"/>
                <rect class="mbb" x="8" y="83" width="115" height="38" rx="2"/>
                <rect class="mb" x="143" y="83" width="130" height="38" rx="2"/>
                <rect class="mbb" x="290" y="83" width="122" height="38" rx="2"/>
                <circle cx="210" cy="72" r="14" fill="var(--accent)" opacity=".9"/>
                <circle cx="210" cy="72" r="6" fill="white"/>
                <circle cx="210" cy="72" r="24" fill="var(--accent)" opacity=".18"/>
              </svg>
              <span class="dmp-label">${l.neighborhood}, ${l.city}</span>
            </div>
          </div>
        </div>

        <div class="detail-sidebar">
          <div class="contact-box">
            <div class="agent-row">
              <div class="agent-avi"><img src="${l.agent.avatar}" alt="${l.agent.name}"
                   onerror="this.src='https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&q=80'" /></div>
              <div>
                <div class="agent-name">${l.agent.name}</div>
                <div class="agent-role">${l.agent.title}</div>
                <div class="agent-stars">${'★'.repeat(Math.floor(l.agent.rating))} <span style="color:var(--muted);font-size:11px">${l.agent.rating} · ${l.agent.reviews} reviews</span></div>
              </div>
            </div>
            <input type="text" placeholder="Your name" />
            <input type="email" placeholder="Email address" />
            <input type="tel" placeholder="Phone (optional)" />
            <textarea rows="3" placeholder="I'm interested in this property…">${l.address}</textarea>
            <button class="btn-send" onclick="showToast('Message sent! The agent will be in touch.')">Contact agent</button>
            <button class="btn-tour" onclick="showToast('Tour requested! Check your email for confirmation.')">Request a tour</button>
            <p class="contact-note">Haven never shares your contact info without your permission.</p>
          </div>
        </div>
      </div>
    </div>`;

  showView('detail');
}

function switchThumb(el, src) {
  document.querySelectorAll('.detail-thumb').forEach(t => t.classList.remove('active'));
  el.classList.add('active');
  const hero = document.getElementById('detail-hero');
  if (hero) hero.src = src;
}

function toggleFavDetail(id, btn) {
  const isFav = state.favorites.has(id);
  if (isFav) {
    state.favorites.delete(id);
    showToast('Removed from saved homes');
  } else {
    state.favorites.add(id);
    showToast('Saved ♥');
  }
  const svg = btn.querySelector('svg');
  const fill  = state.favorites.has(id) ? '#B84A2E' : 'none';
  const stroke = state.favorites.has(id) ? '#B84A2E' : 'currentColor';
  svg.setAttribute('fill', fill);
  svg.setAttribute('stroke', stroke);
}

/* ─── MODAL ─── */
function showModal(type) {
  const bg = document.getElementById('modal-bg');
  const body = document.getElementById('modal-body');
  if (type === 'login') {
    body.innerHTML = `
      <h2>Welcome back</h2>
      <p>Sign in to access your saved homes and searches.</p>
      <input type="email" placeholder="Email address" />
      <input type="password" placeholder="Password" />
      <button class="modal-cta" onclick="closeModal();showToast('Welcome back!')">Sign in</button>
      <p class="modal-foot">New to Haven? <a onclick="showModal('signup')">Create an account</a></p>`;
  } else {
    body.innerHTML = `
      <h2>Join Haven</h2>
      <p>Find your next home with transparent pricing and no hidden fees.</p>
      <input type="text" placeholder="Full name" />
      <input type="email" placeholder="Email address" />
      <input type="password" placeholder="Create a password" />
      <button class="modal-cta" onclick="closeModal();showToast('Welcome to Haven!')">Create account</button>
      <p class="modal-foot">Already a member? <a onclick="showModal('login')">Sign in</a></p>`;
  }
  bg.classList.add('open');
}
function closeModal() { document.getElementById('modal-bg').classList.remove('open'); }

/* ─── TOAST ─── */
let _toastTimer;
function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(_toastTimer);
  _toastTimer = setTimeout(() => t.classList.remove('show'), 2800);
}

/* ─── INIT ─── */
document.addEventListener('DOMContentLoaded', renderFeatured);
