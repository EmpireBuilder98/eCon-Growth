from pathlib import Path

BOOK = Path('/home/ubuntu/econ-growth/book.html')
text = BOOK.read_text()

start_anchor = '<script>\n/* ══════════════════════════════════════════════'
end_anchor = '</script>\n<script src="https://accounts.google.com/gsi/client" onload="gisInit()" onerror="initCalendarFallback()" async defer></script>\n\n<!-- Google Calendar API -->\n<script src="https://apis.google.com/js/api.js" onload="gapiInit()" onerror="initFallback()" async defer></script>\n<script src="https://accounts.google.com/gsi/client" onload="gisInit()" onerror="initFallback()" async defer></script>\n\n<script>'

start = text.find(start_anchor)
end = text.find(end_anchor)
if start == -1 or end == -1 or end <= start:
    raise SystemExit('Could not locate the existing booking calendar block.')

replacement = '''<script>
const BOOKING_API_URL = 'BOOKING_API_URL_PLACEHOLDER';
const TIMEZONE = 'America/Denver';
const SLOT_MINUTES = 30;
const SLOT_TIMES = ['09:00','09:30','10:00','10:30','11:00','11:30','14:00','14:30','15:00','15:30','16:00','16:30'];

let availabilityByDate = {};
let selectedDate = null;
let selectedTime = null;
let currentMonth = new Date();
currentMonth.setDate(1);

function showDateStep(){
  document.getElementById('dateStep').style.display='block';
  document.getElementById('timeStep').classList.remove('active');
  document.getElementById('confirmStep').classList.remove('active');
  document.getElementById('successStep').classList.remove('active');
}

function showTimeStep(){
  document.getElementById('dateStep').style.display='none';
  document.getElementById('timeStep').classList.add('active');
  document.getElementById('confirmStep').classList.remove('active');
  document.getElementById('successStep').classList.remove('active');
  renderTimeSlots(selectedDate);
}

function showConfirmStep(){
  document.getElementById('dateStep').style.display='none';
  document.getElementById('timeStep').classList.remove('active');
  document.getElementById('confirmStep').classList.add('active');
  document.getElementById('successStep').classList.remove('active');
  updateConfirmSummary();
}

function showSuccessStep(){
  document.getElementById('confirmStep').classList.remove('active');
  document.getElementById('successStep').classList.add('active');
}

function fmtDate(d){
  return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
}

function fmtMonth(d){
  return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0');
}

function fmtDateDisplay(ds){
  const [y,m,d]=ds.split('-').map(Number);
  const date=new Date(y,m-1,d);
  const days=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  const months=['January','February','March','April','May','June','July','August','September','October','November','December'];
  return days[date.getDay()]+', '+months[date.getMonth()]+' '+d+', '+y;
}

function fmtTimeDisplay(time24){
  const [hour,minute]=time24.split(':').map(Number);
  const suffix=hour>=12?'PM':'AM';
  const normalized=((hour+11)%12)+1;
  return normalized+':'+String(minute).padStart(2,'0')+' '+suffix;
}

function setStatus(html){
  const el=document.getElementById('calStatus');
  if(el) el.innerHTML=html;
}

function getBookableSlots(ds){
  return Array.isArray(availabilityByDate[ds]) ? availabilityByDate[ds] : [];
}

function isDayFullyBusy(ds){
  return getBookableSlots(ds).length===0;
}

function changeMonth(dir){
  currentMonth.setMonth(currentMonth.getMonth()+dir);
  selectedDate = null;
  selectedTime = null;
  renderCalendar();
  fetchAvailability();
}

function renderCalendar(){
  const now = new Date();
  const year = currentMonth.getFullYear();
  const month = currentMonth.getMonth();
  const months = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  document.getElementById('monthLabel').textContent = months[month]+' '+year;

  const firstDay = new Date(year,month,1).getDay();
  const daysInMonth = new Date(year,month+1,0).getDate();
  let html = ['Su','Mo','Tu','We','Th','Fr','Sa'].map((d)=>`<div class="cal-dow">${d}</div>`).join('');

  for(let i=0;i<firstDay;i++) html += '<div class="cal-day empty"></div>';

  for(let d=1; d<=daysInMonth; d++){
    const date = new Date(year,month,d);
    const dateStr = fmtDate(date);
    const isPast = date < new Date(now.getFullYear(),now.getMonth(),now.getDate());
    const isWeekend = date.getDay()===0 || date.getDay()===6;
    const isToday = dateStr===fmtDate(now);
    const isSelected = selectedDate===dateStr;
    const fullyBusy = !isPast && !isWeekend && isDayFullyBusy(dateStr);

    let cls='cal-day';
    if(isPast || isWeekend) cls+=' disabled';
    else if(fullyBusy) cls+=' busy';
    else cls+=' available';
    if(isToday) cls+=' today';
    if(isSelected) cls+=' selected';

    const click = (!isPast && !isWeekend && !fullyBusy) ? `onclick="selectDate('${dateStr}')"` : '';
    html += `<div class="${cls}" ${click}>${d}</div>`;
  }

  document.getElementById('calGrid').innerHTML = html;
}

function renderTimeSlots(ds){
  const available = getBookableSlots(ds);
  let anyAvail = false;
  let html = '';

  SLOT_TIMES.forEach((timeValue)=>{
    const busy = !available.includes(timeValue);
    const display = fmtTimeDisplay(timeValue);
    const selected = selectedTime===timeValue ? ' selected' : '';
    if(!busy) anyAvail = true;
    html += `<div class="time-slot${busy ? ' busy' : selected}" ${busy ? '' : `onclick="selectTime('${timeValue}')"`}>${display} MT</div>`;
  });

  if(!anyAvail){
    html = '<div class="time-no-slots">No available times on this date.<br>Please pick another day.</div>';
  }

  document.getElementById('timeSlots').innerHTML = html;
}

function selectDate(ds){
  selectedDate = ds;
  selectedTime = null;
  renderCalendar();
  document.getElementById('timeDateHeader').textContent = fmtDateDisplay(ds);
  showTimeStep();
}

function selectTime(timeValue){
  selectedTime = timeValue;
  document.querySelectorAll('.time-slot').forEach((el)=>{
    el.classList.toggle('selected', el.textContent.trim().startsWith(fmtTimeDisplay(timeValue)));
  });
  setTimeout(showConfirmStep, 220);
}

function updateConfirmSummary(){
  document.getElementById('confirmSummaryText').innerHTML = `<span>${fmtDateDisplay(selectedDate)}</span><br><span>${fmtTimeDisplay(selectedTime)} MT</span> · ${SLOT_MINUTES}-minute Growth Call`;
}

function apiRequest(action, params={}){
  return new Promise((resolve, reject)=>{
    if(!BOOKING_API_URL || BOOKING_API_URL.includes('PLACEHOLDER')){
      reject(new Error('Booking API URL is not configured yet.'));
      return;
    }

    const callbackName = `__econGrowthBookingCb_${Date.now()}_${Math.floor(Math.random()*100000)}`;
    const query = new URLSearchParams({ action, callback: callbackName, ...params });
    const script = document.createElement('script');
    let timeoutId = null;

    const cleanup = ()=>{
      delete window[callbackName];
      if(script.parentNode) script.parentNode.removeChild(script);
      if(timeoutId) window.clearTimeout(timeoutId);
    };

    timeoutId = window.setTimeout(()=>{
      cleanup();
      reject(new Error('The booking service timed out.'));
    }, 15000);

    window[callbackName] = (payload)=>{
      cleanup();
      if(payload && payload.ok){
        resolve(payload);
      } else {
        reject(new Error((payload && payload.message) || 'The booking service returned an error.'));
      }
    };

    script.onerror = ()=>{
      cleanup();
      reject(new Error('The booking service could not be reached.'));
    };

    script.src = `${BOOKING_API_URL}?${query.toString()}`;
    document.body.appendChild(script);
  });
}

async function fetchAvailability(){
  setStatus('<span class="cal-loading"></span>&nbsp;Checking live availability…');
  try{
    const payload = await apiRequest('availability', { month: fmtMonth(currentMonth), timezone: TIMEZONE });
    availabilityByDate = payload.availability || {};
    renderCalendar();
    setStatus('✓ Live availability — select a date.');
  }catch(error){
    availabilityByDate = {};
    renderCalendar();
    setStatus('Booking service temporarily unavailable. Call (615) 664-9178 or try again shortly.');
    console.warn('Availability error:', error.message);
  }
}

async function submitBooking(){
  const fname=document.getElementById('fname').value.trim();
  const lname=document.getElementById('lname').value.trim();
  const email=document.getElementById('email').value.trim();
  const phone=document.getElementById('phone').value.trim();
  const company=document.getElementById('company').value.trim();
  const trucks=document.getElementById('trucks').value.trim();

  if(!selectedDate || !selectedTime){
    alert('Please choose a date and time first.');
    return;
  }

  if(!fname || !email){
    alert('Please enter your name and email to confirm.');
    return;
  }

  const btn=document.getElementById('bookBtn');
  btn.disabled=true;
  btn.textContent='Booking…';

  try{
    const payload = await apiRequest('book', {
      date: selectedDate,
      time: selectedTime,
      duration: String(SLOT_MINUTES),
      firstName: fname,
      lastName: lname,
      email,
      phone,
      company,
      trucks,
      source: 'econ-growth.com'
    });

    document.getElementById('successDetails').innerHTML = `
      <div class="success-detail-row"><strong>Name:</strong> ${fname} ${lname}</div>
      <div class="success-detail-row"><strong>Date:</strong> ${fmtDateDisplay(selectedDate)}</div>
      <div class="success-detail-row"><strong>Time:</strong> ${fmtTimeDisplay(selectedTime)} MT</div>
      <div class="success-detail-row"><strong>Email:</strong> ${email}</div>
      ${payload.calendarNote ? `<div class="success-detail-row"><strong>Calendar:</strong> ${payload.calendarNote}</div>` : ''}
      ${payload.eventId ? `<div class="success-detail-row"><strong>Booking ID:</strong> ${payload.eventId}</div>` : ''}
    `;

    showSuccessStep();
    fetchAvailability();
  }catch(error){
    const message = error.message || 'Unable to complete the booking right now.';
    alert(message.toLowerCase().includes('slot') ? 'That time was just taken. Please choose another available slot.' : message);
    if(message.toLowerCase().includes('slot')){
      await fetchAvailability();
      showDateStep();
    }
  }finally{
    btn.disabled=false;
    btn.textContent='Confirm My Growth Call →';
  }
}

window.addEventListener('load', ()=>{
  const authBtn = document.getElementById('authBtn');
  if(authBtn) authBtn.style.display='none';
  renderCalendar();
  fetchAvailability();
});

window.addEventListener('scroll', ()=>{
  document.getElementById('nav').classList.toggle('scrolled', window.scrollY>10);
});

document.addEventListener('DOMContentLoaded', ()=>{
  document.getElementById('nav').classList.add('scrolled');
});
</script>

<script>'''

updated = text[:start] + replacement + text[end + len(end_anchor):]
BOOK.write_text(updated)
print('Updated book.html')
