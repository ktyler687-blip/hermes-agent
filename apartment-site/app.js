/* ===== DATA ===== */
const LISTINGS = [
  {
    id: 1, price: 2850, type: 'apartment', city: 'New York',
    address: '245 W 72nd St, Apt 8B', neighborhood: 'Upper West Side',
    beds: 2, baths: 1, sqft: 920, daysOnMarket: 3,
    badge: 'new', featured: true,
    amenities: ['pet', 'gym', 'laundry'],
    images: [
      'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=600&q=80',
      'https://images.unsplash.com/photo-1560448204-603b3fc33ddc?w=600&q=80',
      'https://images.unsplash.com/photo-1484154218962-a197022b5858?w=600&q=80',
      'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600&q=80',
    ],
    description: 'Stunning renovated 2-bedroom apartment on the Upper West Side. Features hardwood floors throughout, a chef\'s kitchen with quartz countertops, and a private balcony with Central Park views. The building offers a 24-hour doorman, rooftop deck, and state-of-the-art fitness center.',
    agent: { name: 'Sarah Chen', title: 'Licensed Agent · NestFind', rating: 4.9, reviews: 128, avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&q=80' },
    mapPos: { x: 28, y: 22 },
  },
  {
    id: 2, price: 1750, type: 'apartment', city: 'New York',
    address: '88 Fulton St, Apt 12', neighborhood: 'Financial District',
    beds: 1, baths: 1, sqft: 650, daysOnMarket: 7,
    badge: null, featured: true,
    amenities: ['gym', 'parking', 'pool'],
    images: [
      'https://images.unsplash.com/photo-1536376072261-38c75010e6c9?w=600&q=80',
      'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=600&q=80',
      'https://images.unsplash.com/photo-1565183928294-7063f23ce0f8?w=600&q=80',
    ],
    description: 'Modern 1-bedroom in the heart of the Financial District. Floor-to-ceiling windows with breathtaking city skyline views. Open-concept layout with a sleek kitchen island. Building amenities include an Olympic-size rooftop pool, concierge, and private parking garage.',
    agent: { name: 'James Park', title: 'Senior Agent · NestFind', rating: 4.7, reviews: 92, avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&q=80' },
    mapPos: { x: 55, y: 70 },
  },
  {
    id: 3, price: 4200, type: 'condo', city: 'New York',
    address: '1 Central Park W, Unit 34', neighborhood: 'Columbus Circle',
    beds: 3, baths: 2, sqft: 1480, daysOnMarket: 1,
    badge: 'hot', featured: true,
    amenities: ['pet', 'parking', 'gym', 'pool', 'laundry'],
    images: [
      'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=600&q=80',
      'https://images.unsplash.com/photo-1565182999561-18d7dc61c393?w=600&q=80',
      'https://images.unsplash.com/photo-1556020685-ae41abfc9365?w=600&q=80',
      'https://images.unsplash.com/photo-1560185007-5f0bb1866cab?w=600&q=80',
    ],
    description: 'Exceptional luxury condo overlooking Central Park. This spectacular 3-bedroom residence features a grand entrance foyer, chef\'s kitchen with Sub-Zero appliances, formal dining room, and a master suite with a spa-like bathroom. Full-service white-glove building.',
    agent: { name: 'Mia Torres', title: 'Luxury Specialist · NestFind', rating: 5.0, reviews: 214, avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&q=80' },
    mapPos: { x: 38, y: 30 },
  },
  {
    id: 4, price: 1350, type: 'apartment', city: 'Chicago',
    address: '2111 N Clark St, Apt 304', neighborhood: 'Lincoln Park',
    beds: 1, baths: 1, sqft: 710, daysOnMarket: 14,
    badge: 'drop', featured: false,
    amenities: ['pet', 'laundry'],
    images: [
      'https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=600&q=80',
      'https://images.unsplash.com/photo-1556228453-efd6c1ff04f6?w=600&q=80',
    ],
    description: 'Charming updated 1-bedroom in vibrant Lincoln Park. Exposed brick, original hardwood floors, and a sunny bay window. Steps from the lakefront trail, world-class dining, and the Lincoln Park Zoo. Price recently reduced — don\'t miss this one!',
    agent: { name: 'Tyler Brooks', title: 'Licensed Agent · NestFind', rating: 4.6, reviews: 57, avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&q=80' },
    mapPos: { x: 20, y: 45 },
  },
  {
    id: 5, price: 2100, type: 'condo', city: 'Chicago',
    address: '400 N Lake Shore Dr, Unit 1802', neighborhood: 'Streeterville',
    beds: 2, baths: 2, sqft: 1050, daysOnMarket: 5,
    badge: 'new', featured: false,
    amenities: ['gym', 'pool', 'parking', 'laundry'],
    images: [
      'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=600&q=80',
      'https://images.unsplash.com/photo-1560185008-b033106af5c3?w=600&q=80',
      'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&q=80',
    ],
    description: 'Gorgeous lake-view condo in one of Chicago\'s most sought-after buildings. Bright open floor plan with updated kitchen, in-unit washer/dryer, and a large private balcony facing Lake Michigan. Building amenities include indoor pool, fitness center, and 24-hour security.',
    agent: { name: 'Sarah Chen', title: 'Licensed Agent · NestFind', rating: 4.9, reviews: 128, avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&q=80' },
    mapPos: { x: 65, y: 38 },
  },
  {
    id: 6, price: 3600, type: 'house', city: 'Miami',
    address: '740 NE 13th Ave', neighborhood: 'Edgewater',
    beds: 3, baths: 2, sqft: 1650, daysOnMarket: 9,
    badge: null, featured: true,
    amenities: ['pet', 'parking', 'pool'],
    images: [
      'https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=600&q=80',
      'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&q=80',
      'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=600&q=80',
    ],
    description: 'Stunning modern home in Edgewater with biscayne bay views. Open concept living with high ceilings, impact windows throughout, and a resort-style backyard with heated pool and summer kitchen. Smart home technology and solar panels included. A rare gem in Miami real estate.',
    agent: { name: 'Mia Torres', title: 'Luxury Specialist · NestFind', rating: 5.0, reviews: 214, avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&q=80' },
    mapPos: { x: 45, y: 55 },
  },
  {
    id: 7, price: 1950, type: 'apartment', city: 'Los Angeles',
    address: '1412 S Figueroa St, Apt 201', neighborhood: 'South Park',
    beds: 1, baths: 1, sqft: 780, daysOnMarket: 2,
    badge: 'new', featured: false,
    amenities: ['gym', 'pool', 'parking'],
    images: [
      'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=600&q=80',
      'https://images.unsplash.com/photo-1565183928294-7063f23ce0f8?w=600&q=80',
    ],
    description: 'Sleek modern 1-bedroom in the heart of Downtown LA\'s South Park neighborhood. High-end finishes throughout with a designer kitchen, spa bathroom, and expansive city views. Walking distance to Staples Center, LA Live, and the city\'s best restaurants.',
    agent: { name: 'James Park', title: 'Senior Agent · NestFind', rating: 4.7, reviews: 92, avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&q=80' },
    mapPos: { x: 30, y: 60 },
  },
  {
    id: 8, price: 3200, type: 'condo', city: 'Los Angeles',
    address: '888 S Olive St, Unit 1502', neighborhood: 'Bunker Hill',
    beds: 2, baths: 2, sqft: 1210, daysOnMarket: 4,
    badge: 'featured', featured: false,
    amenities: ['pet', 'gym', 'parking', 'pool', 'laundry'],
    images: [
      'https://images.unsplash.com/photo-1560184897-ae75f418493e?w=600&q=80',
      'https://images.unsplash.com/photo-1571508601891-ca5e7a713859?w=600&q=80',
      'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600&q=80',
    ],
    description: 'Exquisite high-rise condo with panoramic views of the LA skyline, mountains, and ocean. Features a gourmet kitchen, expansive primary suite, and a wraparound terrace. The tower offers a resort-style pool deck, wine cellar, screening room, and private dog park.',
    agent: { name: 'Tyler Brooks', title: 'Licensed Agent · NestFind', rating: 4.6, reviews: 57, avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&q=80' },
    mapPos: { x: 72, y: 25 },
  },
  {
    id: 9, price: 2400, type: 'apartment', city: 'Seattle',
    address: '2001 8th Ave, Apt 15B', neighborhood: 'Belltown',
    beds: 2, baths: 1, sqft: 960, daysOnMarket: 6,
    badge: null, featured: false,
    amenities: ['pet', 'gym', 'laundry'],
    images: [
      'https://images.unsplash.com/photo-1484101403633-562f891dc89a?w=600&q=80',
      'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=600&q=80',
    ],
    description: 'Spacious 2-bedroom apartment with stunning Puget Sound and Olympic Mountain views. Open layout with polished concrete floors, a gourmet kitchen with waterfall island, and a private deck. Located in vibrant Belltown with walkable access to Pike Place Market.',
    agent: { name: 'Sarah Chen', title: 'Licensed Agent · NestFind', rating: 4.9, reviews: 128, avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&q=80' },
    mapPos: { x: 50, y: 40 },
  },
  {
    id: 10, price: 1600, type: 'apartment', city: 'Austin',
    address: '604 W 6th St, Unit 302', neighborhood: 'West 6th',
    beds: 1, baths: 1, sqft: 720, daysOnMarket: 11,
    badge: 'drop', featured: false,
    amenities: ['pet', 'gym', 'pool'],
    images: [
      'https://images.unsplash.com/photo-1560448204-603b3fc33ddc?w=600&q=80',
      'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=600&q=80',
    ],
    description: 'Hip 1-bedroom loft steps from Austin\'s legendary 6th Street entertainment district. Industrial chic with exposed duct work, a stylish kitchen, and an oversized rooftop terrace. Price reduced for quick lease. Pet friendly — large dogs welcome. SXSW and ACL are right outside your door.',
    agent: { name: 'James Park', title: 'Senior Agent · NestFind', rating: 4.7, reviews: 92, avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&q=80' },
    mapPos: { x: 60, y: 65 },
  },
  {
    id: 11, price: 5500, type: 'condo', city: 'Miami',
    address: '1000 Brickell Plaza, PH 48', neighborhood: 'Brickell',
    beds: 3, baths: 3, sqft: 2100, daysOnMarket: 2,
    badge: 'hot', featured: false,
    amenities: ['pet', 'gym', 'parking', 'pool', 'laundry'],
    images: [
      'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=600&q=80',
      'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=600&q=80',
      'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=600&q=80',
    ],
    description: 'Extraordinary penthouse at the top of Brickell\'s most iconic tower. This 3-bedroom sky mansion features 12-foot ceilings, a private rooftop terrace with plunge pool, and 360° views of Biscayne Bay and the Miami skyline. Ultra-luxury amenities across 5 floors.',
    agent: { name: 'Mia Torres', title: 'Luxury Specialist · NestFind', rating: 5.0, reviews: 214, avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&q=80' },
    mapPos: { x: 35, y: 75 },
  },
  {
    id: 12, price: 1100, type: 'apartment', city: 'Chicago',
    address: '3245 N Halsted St, Apt 2', neighborhood: 'Boystown',
    beds: 0, baths: 1, sqft: 480, daysOnMarket: 20,
    badge: null, featured: false,
    amenities: ['laundry'],
    images: [
      'https://images.unsplash.com/photo-1536376072261-38c75010e6c9?w=600&q=80',
    ],
    description: 'Cozy studio apartment in the heart of Boystown. Recently updated with new kitchen appliances, fresh paint, and refinished hardwood floors. Coin laundry in building. Walk to the L train, restaurants, shops, and Wrigley Field. Utilities included in rent.',
    agent: { name: 'Tyler Brooks', title: 'Licensed Agent · NestFind', rating: 4.6, reviews: 57, avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&q=80' },
    mapPos: { x: 80, y: 50 },
  },
  {
    id: 13, price: 2900, type: 'townhouse', city: 'Austin',
    address: '1805 E Cesar Chavez St', neighborhood: 'East Austin',
    beds: 3, baths: 2, sqft: 1380, daysOnMarket: 8,
    badge: 'new', featured: false,
    amenities: ['pet', 'parking', 'laundry'],
    images: [
      'https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=600&q=80',
      'https://images.unsplash.com/photo-1480074568708-e7b720bb3f09?w=600&q=80',
    ],
    description: 'Modern townhouse in the heart of trendy East Austin. Thoughtful layout with private fenced yard, attached garage, and a rooftop deck. Chef\'s kitchen with quartz countertops and farmhouse sink. Walkable to breweries, coffee shops, and the famous Franklin Barbecue.',
    agent: { name: 'Sarah Chen', title: 'Licensed Agent · NestFind', rating: 4.9, reviews: 128, avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&q=80' },
    mapPos: { x: 42, y: 58 },
  },
  {
    id: 14, price: 3800, type: 'house', city: 'Seattle',
    address: '4521 Phinney Ave N', neighborhood: 'Phinney Ridge',
    beds: 4, baths: 3, sqft: 2050, daysOnMarket: 3,
    badge: 'featured', featured: false,
    amenities: ['pet', 'parking', 'laundry'],
    images: [
      'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=600&q=80',
      'https://images.unsplash.com/photo-1575517111839-3a3843ee7f5d?w=600&q=80',
    ],
    description: 'Beautifully restored craftsman home on Phinney Ridge with sweeping views of Puget Sound and the Olympic Mountains. Original character preserved with modern updates: new kitchen, master bath, and 200-amp electrical. Lush garden, detached 2-car garage, and mature trees. A true Seattle gem.',
    agent: { name: 'James Park', title: 'Senior Agent · NestFind', rating: 4.7, reviews: 92, avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&q=80' },
    mapPos: { x: 18, y: 32 },
  },
  {
    id: 15, price: 2300, type: 'apartment', city: 'Los Angeles',
    address: '5217 Hollywood Blvd, Apt 8', neighborhood: 'Hollywood',
    beds: 2, baths: 1, sqft: 875, daysOnMarket: 16,
    badge: 'drop', featured: false,
    amenities: ['pool', 'gym'],
    images: [
      'https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=600&q=80',
      'https://images.unsplash.com/photo-1560448204-603b3fc33ddc?w=600&q=80',
    ],
    description: 'Stylish mid-century modern 2-bedroom in the heart of Hollywood. Updated kitchen and baths, hardwood floors, and a private balcony. Resort-style pool and fitness center on premises. Walking distance to the Walk of Fame, Dolby Theatre, and iconic LA nightlife. Price reduced!',
    agent: { name: 'Mia Torres', title: 'Luxury Specialist · NestFind', rating: 5.0, reviews: 214, avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&q=80' },
    mapPos: { x: 68, y: 48 },
  },
  {
    id: 16, price: 4800, type: 'condo', city: 'New York',
    address: '56 Leonard St, Unit 22', neighborhood: 'Tribeca',
    beds: 3, baths: 2, sqft: 1720, daysOnMarket: 1,
    badge: 'hot', featured: false,
    amenities: ['pet', 'gym', 'parking', 'pool', 'laundry'],
    images: [
      'https://images.unsplash.com/photo-1560184897-ae75f418493e?w=600&q=80',
      'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=600&q=80',
      'https://images.unsplash.com/photo-1484154218962-a197022b5858?w=600&q=80',
    ],
    description: 'Magnificent Tribeca loft in the iconic Jenga Tower. Soaring ceilings, floor-to-ceiling windows with Hudson River views, and custom millwork throughout. State-of-the-art kitchen with Wolf and Sub-Zero appliances. The building offers a 75-foot pool, children\'s playroom, and private cinema.',
    agent: { name: 'Sarah Chen', title: 'Licensed Agent · NestFind', rating: 4.9, reviews: 128, avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&q=80' },
    mapPos: { x: 48, y: 78 },
  },
];

/* ===== STATE ===== */
let state = {
  view: 'home',
  filtered: [...LISTINGS],
  currentPage: 1,
  perPage: 8,
  listingView: 'grid',
  favorites: new Set(),
  cityFilter: '',
  typeFilter: '',
  filtersOpen: false,
};

const fmt = n => '$' + n.toLocaleString();
const bedLabel = n => n === 0 ? 'Studio' : n === 1 ? '1 bd' : `${n} bd`;

/* ===== VIEW ROUTER ===== */
function showView(name) {
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  document.getElementById('view-' + name).classList.add('active');
  state.view = name;
  if (name === 'home') renderFeatured();
  if (name === 'listings') { applyFilters(); renderMapPins(); }
  window.scrollTo(0, 0);
}

/* ===== FEATURED ===== */
function renderFeatured() {
  const grid = document.getElementById('featured-grid');
  const featured = LISTINGS.filter(l => l.featured).slice(0, 4);
  grid.innerHTML = featured.map(l => cardHTML(l)).join('');
}

/* ===== PROPERTY CARD HTML ===== */
function cardHTML(listing, mode = 'grid') {
  const isFav = state.favorites.has(listing.id);
  const badgeMap = { new: 'badge-new', hot: 'badge-hot', drop: 'badge-drop', featured: 'badge-featured' };
  const badgeLabelMap = { new: 'New', hot: '🔥 Hot', drop: 'Price Drop', featured: 'Featured' };
  const amenityIcons = { pet: 'Pets', gym: 'Gym', pool: 'Pool', parking: 'Parking', laundry: 'W/D' };

  return `
    <div class="property-card ${mode === 'list' ? 'list-view' : ''}" onclick="openDetail(${listing.id})">
      <div class="card-image">
        <img src="${listing.images[0]}" alt="${listing.address}" loading="lazy" onerror="this.src='https://images.unsplash.com/photo-1486325212027-8081e485255e?w=600&q=80'" />
        ${listing.badge ? `<span class="card-badge ${badgeMap[listing.badge]}">${badgeLabelMap[listing.badge]}</span>` : ''}
        <button class="card-fav ${isFav ? 'active' : ''}" onclick="toggleFav(event, ${listing.id})">
          <svg viewBox="0 0 24 24" fill="${isFav ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2">
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
          </svg>
        </button>
        ${listing.images.length > 1 ? `
        <span class="card-photo-count">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
          ${listing.images.length}
        </span>` : ''}
      </div>
      <div class="card-body">
        <div class="card-price">${fmt(listing.price)}<span>/mo</span></div>
        <div class="card-address">${listing.address}</div>
        <div class="card-meta">
          <span>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
            ${bedLabel(listing.beds)}
          </span>
          <span class="dot"></span>
          <span>${listing.baths} ba</span>
          <span class="dot"></span>
          <span>${listing.sqft.toLocaleString()} sqft</span>
        </div>
      </div>
      <div class="card-footer">
        <span class="card-days">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          ${listing.daysOnMarket}d ago
        </span>
        <div class="card-amenity-tags">
          ${listing.amenities.slice(0, 3).map(a => `<span class="amenity-tag">${amenityIcons[a]}</span>`).join('')}
        </div>
      </div>
    </div>`;
}

/* ===== FILTERS ===== */
function applyFilters() {
  const search = (document.getElementById('listing-search-input')?.value || '').toLowerCase();
  const beds = document.getElementById('filter-beds')?.value || '';
  const price = parseInt(document.getElementById('filter-price')?.value || '0');
  const type = document.getElementById('filter-type')?.value || state.typeFilter || '';
  const baths = parseInt(document.getElementById('filter-baths')?.value || '0');
  const sqftMin = parseInt(document.getElementById('filter-sqft-min')?.value || '0');
  const sqftMax = parseInt(document.getElementById('filter-sqft-max')?.value || '999999');
  const sortBy = document.getElementById('filter-sort')?.value || 'newest';
  const petFriendly = document.getElementById('filter-pet')?.checked;
  const hasParking = document.getElementById('filter-parking')?.checked;
  const hasGym = document.getElementById('filter-gym')?.checked;
  const hasPool = document.getElementById('filter-pool')?.checked;
  const hasLaundry = document.getElementById('filter-laundry')?.checked;

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
    if (price && l.price > price) return false;
    if (type && l.type !== type) return false;
    if (baths && l.baths < baths) return false;
    if (l.sqft < sqftMin || l.sqft > sqftMax) return false;
    if (petFriendly && !l.amenities.includes('pet')) return false;
    if (hasParking && !l.amenities.includes('parking')) return false;
    if (hasGym && !l.amenities.includes('gym')) return false;
    if (hasPool && !l.amenities.includes('pool')) return false;
    if (hasLaundry && !l.amenities.includes('laundry')) return false;
    return true;
  });

  results.sort((a, b) => {
    if (sortBy === 'price-low') return a.price - b.price;
    if (sortBy === 'price-high') return b.price - a.price;
    if (sortBy === 'sqft') return b.sqft - a.sqft;
    return a.daysOnMarket - b.daysOnMarket; // newest
  });

  state.filtered = results;
  state.currentPage = 1;
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
  const val = document.getElementById('hero-search-input').value;
  if (val) {
    const input = document.getElementById('listing-search-input');
    if (input) input.value = val;
  }
  showView('listings');
}

/* ===== RENDER LISTINGS ===== */
function renderListings() {
  const grid = document.getElementById('listings-grid');
  const countEl = document.getElementById('listing-count');
  if (!grid) return;

  const total = state.filtered.length;
  const start = (state.currentPage - 1) * state.perPage;
  const page = state.filtered.slice(start, start + state.perPage);
  const mode = state.listingView;

  countEl.textContent = `${total} home${total !== 1 ? 's' : ''}`;
  grid.className = 'listings-grid' + (mode === 'list' ? ' list-mode' : '');
  grid.innerHTML = page.length
    ? page.map(l => cardHTML(l, mode)).join('')
    : '<div style="grid-column:1/-1;padding:48px;text-align:center;color:#6b7280;font-size:15px;">No listings match your filters.<br><a href="#" style="color:#cc0000;font-weight:500;margin-top:8px;display:inline-block;" onclick="clearFilters();return false;">Clear all filters</a></div>';

  renderPagination(total);
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
  const si = document.getElementById('listing-search-input');
  if (si) si.value = '';
  applyFilters();
}

function renderPagination(total) {
  const pag = document.getElementById('pagination');
  if (!pag) return;
  const pages = Math.ceil(total / state.perPage);
  if (pages <= 1) { pag.innerHTML = ''; return; }
  let html = '';
  if (state.currentPage > 1) html += `<button class="page-btn" onclick="goPage(${state.currentPage - 1})">‹</button>`;
  for (let i = 1; i <= pages; i++) {
    if (i === 1 || i === pages || Math.abs(i - state.currentPage) <= 1) {
      html += `<button class="page-btn ${i === state.currentPage ? 'active' : ''}" onclick="goPage(${i})">${i}</button>`;
    } else if (Math.abs(i - state.currentPage) === 2) {
      html += `<span class="page-btn dots">…</span>`;
    }
  }
  if (state.currentPage < pages) html += `<button class="page-btn" onclick="goPage(${state.currentPage + 1})">›</button>`;
  pag.innerHTML = html;
}

function goPage(p) {
  state.currentPage = p;
  renderListings();
  document.getElementById('listings-panel').scrollTo({ top: 0, behavior: 'smooth' });
}

/* ===== VIEW TOGGLE ===== */
function setListingView(v) {
  state.listingView = v;
  document.getElementById('view-grid-btn').classList.toggle('active', v === 'grid');
  document.getElementById('view-list-btn').classList.toggle('active', v === 'list');
  renderListings();
}

/* ===== FILTERS TOGGLE ===== */
function toggleFilters() {
  state.filtersOpen = !state.filtersOpen;
  const panel = document.getElementById('extra-filters');
  const btn = document.querySelector('.btn-more-filters');
  panel.style.display = state.filtersOpen ? 'block' : 'none';
  btn.classList.toggle('active', state.filtersOpen);
}

/* ===== FAVORITES ===== */
function toggleFav(e, id) {
  e.stopPropagation();
  if (state.favorites.has(id)) {
    state.favorites.delete(id);
    showToast('Removed from saved homes');
  } else {
    state.favorites.add(id);
    showToast('Saved to your favorites ♥');
  }
  renderListings();
  if (state.view === 'home') renderFeatured();
}

/* ===== MAP PINS ===== */
function renderMapPins() {
  const container = document.getElementById('map-pins');
  if (!container) return;
  const start = (state.currentPage - 1) * state.perPage;
  const page = state.filtered.slice(start, start + state.perPage);
  container.innerHTML = page.map(l => `
    <div class="map-pin" style="left:${l.mapPos.x}%;top:${l.mapPos.y}%;" onclick="openDetail(${l.id})">
      <div class="pin-bubble">${fmt(l.price)}</div>
      <div class="pin-tooltip">
        <strong>${fmt(l.price)}/mo</strong>
        <span>${bedLabel(l.beds)} · ${l.sqft} sqft<br>${l.neighborhood}</span>
      </div>
    </div>`).join('');
}

function mapZoom(dir) {
  showToast(dir > 0 ? 'Zoomed in' : 'Zoomed out');
}
function toggleMap() {
  const mapPanel = document.getElementById('map-panel');
  const btn = document.querySelector('.map-toggle-btn');
  if (mapPanel.style.display === 'none') {
    mapPanel.style.display = '';
    btn.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/></svg>Hide Map`;
  } else {
    mapPanel.style.display = 'none';
    btn.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/></svg>Show Map`;
  }
}

/* ===== PROPERTY DETAIL ===== */
function openDetail(id) {
  const l = LISTINGS.find(x => x.id === id);
  if (!l) return;
  const container = document.getElementById('detail-container');
  const stars = '★'.repeat(Math.floor(l.agent.rating)) + (l.agent.rating % 1 >= 0.5 ? '½' : '');
  const featureList = [
    { icon: '<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>', label: `${bedLabel(l.beds)} Bedroom${l.beds > 1 ? 's' : ''}` },
    { icon: '<path d="M4 12h16"/><path d="M4 6h16"/><path d="M4 18h7"/>', label: `${l.baths} Bathroom${l.baths > 1 ? 's' : ''}` },
    { icon: '<rect x="3" y="3" width="18" height="18" rx="2"/>', label: `${l.sqft.toLocaleString()} sq ft` },
    ...(l.amenities.includes('pet') ? [{ icon: '<circle cx="12" cy="12" r="3"/><path d="M6.4 20a9 9 0 1 1 11.2 0"/>', label: 'Pet Friendly' }] : []),
    ...(l.amenities.includes('gym') ? [{ icon: '<path d="M6.5 6.5h11"/><path d="M6.5 17.5h11"/><path d="M6.5 6.5v11"/><path d="M17.5 6.5v11"/>', label: 'Fitness Center' }] : []),
    ...(l.amenities.includes('pool') ? [{ icon: '<path d="M2 12h20M2 12c0-5.5 3-8 5-8s5 2.5 5 8-3 8-5 8-5-2.5-5-8zm20 0c0-5.5-3-8-5-8"/>', label: 'Swimming Pool' }] : []),
    ...(l.amenities.includes('parking') ? [{ icon: '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 17V7h4a3 3 0 0 1 0 6H9"/>', label: 'Parking' }] : []),
    ...(l.amenities.includes('laundry') ? [{ icon: '<rect x="2" y="4" width="20" height="20" rx="2"/><path d="M12 14a4 4 0 1 0 0-8 4 4 0 0 0 0 8z"/>', label: 'In-Unit Laundry' }] : []),
  ];

  const galleryItems = l.images.slice(1, 3).map((img, i) =>
    i === 1 && l.images.length > 3
      ? `<div class="gallery-item more-photos" data-count="${l.images.length - 3}"><img src="${img}" alt="" /></div>`
      : `<div class="gallery-item"><img src="${img}" alt="" /></div>`
  ).join('');

  container.innerHTML = `
    <button class="detail-back" onclick="showView('listings')">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg>
      Back to listings
    </button>

    <div class="detail-gallery">
      <div class="gallery-main"><img src="${l.images[0]}" alt="${l.address}" /></div>
      ${galleryItems}
    </div>

    <div class="detail-layout">
      <div class="detail-main">
        <div class="detail-price-row">
          <div>
            <div class="detail-price">${fmt(l.price)}<small>/mo</small></div>
            <div class="detail-address">${l.address} · ${l.neighborhood}, ${l.city}</div>
          </div>
          <div class="detail-actions">
            <button class="detail-action-btn" onclick="toggleFav(event,${l.id})" title="Save">
              <svg viewBox="0 0 24 24" fill="${state.favorites.has(l.id) ? '#cc0000' : 'none'}" stroke="${state.favorites.has(l.id) ? '#cc0000' : 'currentColor'}" stroke-width="2">
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
              </svg>
            </button>
            <button class="detail-action-btn" onclick="shareDetail()" title="Share">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
            </button>
          </div>
        </div>

        <div class="detail-stats">
          <div class="detail-stat"><strong>${l.beds === 0 ? '—' : l.beds}</strong><span>${l.beds === 0 ? 'Studio' : 'Beds'}</span></div>
          <div class="detail-stat"><strong>${l.baths}</strong><span>Baths</span></div>
          <div class="detail-stat"><strong>${l.sqft.toLocaleString()}</strong><span>Sq Ft</span></div>
          <div class="detail-stat"><strong>${l.daysOnMarket}d</strong><span>On Market</span></div>
          <div class="detail-stat"><strong>${l.type.charAt(0).toUpperCase() + l.type.slice(1)}</strong><span>Type</span></div>
        </div>

        <div class="detail-section">
          <h3>About this Home</h3>
          <p class="detail-description">${l.description}</p>
        </div>

        <div class="detail-section">
          <h3>Features & Amenities</h3>
          <div class="detail-features">
            ${featureList.map(f => `
              <div class="feature-item">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">${f.icon}</svg>
                ${f.label}
              </div>`).join('')}
          </div>
        </div>

        <div class="detail-section">
          <h3>Location</h3>
          <div class="detail-map-preview">
            <svg viewBox="0 0 400 180" preserveAspectRatio="xMidYMid slice">
              <defs><pattern id="dgrid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M 30 0 L 0 0 0 30" fill="none" stroke="#d1d5db" stroke-width="0.5"/></pattern></defs>
              <rect width="100%" height="100%" fill="#e8eff8"/>
              <rect width="100%" height="100%" fill="url(#dgrid)"/>
              <rect x="0" y="70" width="400" height="8" fill="#fff" opacity="0.9"/>
              <rect x="0" y="120" width="400" height="6" fill="#fff" opacity="0.9"/>
              <rect x="150" y="0" width="8" height="180" fill="#fff" opacity="0.9"/>
              <rect x="280" y="0" width="6" height="180" fill="#fff" opacity="0.9"/>
              <circle cx="200" cy="90" r="12" fill="#cc0000" opacity="0.9"/>
              <circle cx="200" cy="90" r="6" fill="white"/>
              <circle cx="200" cy="90" r="22" fill="#cc0000" opacity="0.15"/>
            </svg>
            <span style="position:absolute;bottom:10px;left:50%;transform:translateX(-50%);background:rgba(255,255,255,0.9);padding:3px 10px;border-radius:12px;font-size:12px;color:#374151;font-weight:500;">${l.neighborhood}, ${l.city}</span>
          </div>
        </div>
      </div>

      <div class="detail-sidebar">
        <div class="contact-card">
          <div class="contact-card-header">
            <div class="agent-avatar"><img src="${l.agent.avatar}" alt="${l.agent.name}" /></div>
            <div class="agent-info">
              <div class="agent-name">${l.agent.name}</div>
              <div class="agent-title">${l.agent.title}</div>
              <div class="agent-rating">
                ${'★'.repeat(Math.floor(l.agent.rating))}
                <span style="color:#6b7280">${l.agent.rating} (${l.agent.reviews} reviews)</span>
              </div>
            </div>
          </div>
          <input type="text" placeholder="Your name" />
          <input type="email" placeholder="Email address" />
          <input type="tel" placeholder="Phone number" />
          <textarea rows="3" placeholder="I'm interested in this property and would love to schedule a tour...">${l.address}</textarea>
          <button class="btn-contact" onclick="submitContact()">Contact Agent</button>
          <button class="btn-tour" onclick="submitTour()">Schedule a Tour</button>
          <p class="contact-note">By proceeding, you agree to our Terms of Service and Privacy Policy. NestFind does not share your information without consent.</p>
        </div>
      </div>
    </div>`;

  showView('detail');
}

function shareDetail() { showToast('Link copied to clipboard!'); }
function submitContact() { showToast('Message sent! The agent will contact you soon.'); }
function submitTour() { showToast('Tour request submitted! Check your email for confirmation.'); }

/* ===== MODAL ===== */
function showModal(type) {
  const overlay = document.getElementById('modal-overlay');
  const content = document.getElementById('modal-content');

  if (type === 'login') {
    content.innerHTML = `
      <h2>Welcome back</h2>
      <p>Sign in to access your saved homes and searches.</p>
      <input type="email" placeholder="Email address" />
      <input type="password" placeholder="Password" />
      <button class="modal-submit" onclick="submitLogin()">Sign In</button>
      <p class="modal-footer">Don't have an account? <a onclick="showModal('signup')">Sign up free</a></p>`;
  } else {
    content.innerHTML = `
      <h2>Create your account</h2>
      <p>Join thousands of renters finding their perfect home.</p>
      <input type="text" placeholder="Full name" />
      <input type="email" placeholder="Email address" />
      <input type="password" placeholder="Create a password" />
      <button class="modal-submit" onclick="submitSignup()">Create Account</button>
      <p class="modal-footer">Already have an account? <a onclick="showModal('login')">Sign in</a></p>`;
  }
  overlay.classList.add('open');
}

function closeModal() { document.getElementById('modal-overlay').classList.remove('open'); }
function submitLogin() { closeModal(); showToast('Welcome back!'); }
function submitSignup() { closeModal(); showToast('Account created! Welcome to NestFind.'); }

/* ===== TOAST ===== */
let toastTimer;
function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove('show'), 2800);
}

/* ===== INIT ===== */
document.addEventListener('DOMContentLoaded', () => {
  renderFeatured();
});
