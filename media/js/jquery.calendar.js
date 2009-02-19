/* MarcGrabanski.com v2.3 */
/* Pop-Up Calendar Built from Scratch by Marc Grabanski */
/* Enhanced by Keith Wood (kbwood@iprimus.com.au). */
/* Under the Creative Commons Licence http://creativecommons.org/licenses/by/3.0/
	Share or Remix it but please Attribute the authors. */
var popUpCal = {
	selectedDay: new Date().getDate(),
	selectedMonth: new Date().getMonth(), // 0-11
	selectedYear: new Date().getFullYear(), // 4-digit year
	clearText: 'Limpar', // Display text for clear link
	closeText: 'Fechar', // Display text for close link
	prevText: '&lt;Ant', // Display text for previous month link
	nextText: 'Prox&gt;', // Display text for next month link
	currentText: 'Hoje', // Display text for current month link
	appendText: '', // Display text following the input box, e.g. showing the format
	buttonText: '...', // Text for trigger button
	buttonImage: '', // URL for trigger button image
	buttonImageOnly: false, // True if the image appears alone, false if it appears on a button
	dayNames: new Array('Dom','Seg','Ter','Qua','Qui','Sex','Sab'), // Names of days starting at Sunday
	monthNames: new Array('Janeiro','Fevereiro','Mar&ccedil;o','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'), // Names of months
	dateFormat: 'DMY/', // First three are day, month, year in the required order, fourth is the separator, e.g. US would be 'MDY/'
	yearRange: '-100:+10', // Range of years to display in drop-down, either relative to current year (-nn:+nn) or absolute (nnnn:nnnn)
	firstDay: 0, // The first day of the week, Sun = 0, Mon = 1, ...
	showOtherMonths: false, // True to show dates in other months, false to leave blank
	minDate: null, // The earliest selectable date, or null for no limit
	maxDate: null, // The latest selectable date, or null for no limit
	speed: 'medium', // Speed of display/closure
	autoPopUp: 'focus', // 'focus' for popup on focus, 'button' for trigger button, or 'both' for either
	closeAtTop: true, // True to have the clear/close at the top, false to have them at the bottom
	customDate: null, // Function that takes a date and returns an array with [0] = true if selectable, false if not,
		// [1] = custom CSS class name(s) or '', e.g. popUpCal.noWeekends
	
	init: function() {
		this.popUpShowing = false;
		this.lastInput = null;
		$('body').append('<div id="calendar_div"></div>');
		$(document).mousedown(popUpCal.checkExternalClick);
		this.showFunction = function(target) { // pop-up calendar when triggered
			input = (target.nodeName && target.nodeName.toLowerCase() == 'input' ? target : this);
			if (input.nodeName.toLowerCase() != 'input') { // find from button/image trigger
				input = $('../input', input)[0];
			}
			if (popUpCal.lastInput == input) {
				return;
			}
			popUpCal.input = $(input);
			popUpCal.hideCalendar();
			popUpCal.lastInput = input;
			popUpCal.setDateFromField();
			popUpCal.setPos(input, $('#calendar_div'));
			popUpCal.showCalendar(); 
		};
		this.keyDownFunction = function(e) {
			if (popUpCal.popUpShowing) {
				if (e.keyCode == 9) { // hide on tab out
					popUpCal.hideCalendar();
				}
				else if (e.keyCode == 27) { // hide on escape
					popUpCal.hideCalendar(popUpCal.speed);
				}
				else if (e.keyCode == 33) { // previous month/year on page up/+ ctrl
					popUpCal.adjustDate(-1, (e.ctrlKey ? 'Y' : 'M'));
				}
				else if (e.keyCode == 34) { // next month/year on page down/+ ctrl
					popUpCal.adjustDate(+1, (e.ctrlKey ? 'Y' : 'M'));
				}
				else if (e.keyCode == 35 && e.ctrlKey) { // clear on ctrl+end
					$('#calendar_clear').click();
				}
				else if (e.keyCode == 36 && e.ctrlKey) { // current on ctrl+home
					$('#calendar_current').click();
				}
				else if (e.keyCode == 37 && e.ctrlKey) { // -1 day on ctrl+left
					popUpCal.adjustDate(-1, 'D');
				}
				else if (e.keyCode == 38 && e.ctrlKey) { // -1 week on ctrl+up
					popUpCal.adjustDate(-7, 'D');
				}
				else if (e.keyCode == 39 && e.ctrlKey) { // +1 day on ctrl+right
					popUpCal.adjustDate(+1, 'D');
				}
				else if (e.keyCode == 40 && e.ctrlKey) { // +1 week on ctrl+down
					popUpCal.adjustDate(+7, 'D');
				}
				else if (e.keyCode == 13) { // select the value on enter
					popUpCal.selectDate();
				}
			}
			else if (e.keyCode == 36 && e.ctrlKey) { // display the calendar on ctrl+home
				popUpCal.showFunction(this);
				popUpCal.showCalendar();
			}
		};
		this.keyPressFunction = function(e) {
			chr = String.fromCharCode(e.charCode == undefined ? e.keyCode : e.charCode);
			if (chr > ' ' && chr != popUpCal.dateFormat.charAt(3) && (chr < '0' || chr > '9')) { // only allow numbers and separator
				return false;
			}
			return true;
		};
	}, // end init
	
	connectCalendar: function(target) {
		var $input = $(target);
		$input.after('<span class="calendar_append">' + this.appendText + '</span>');
		if (this.autoPopUp == 'focus' || this.autoPopUp == 'both') { // pop-up calendar when in the marked fields
			$input.focus(this.showFunction);
		}
		if (this.autoPopUp == 'button' || this.autoPopUp == 'both') { // pop-up calendar when button clicked
			$input.wrap('<span class="calendar_wrap"></span>').
				after(this.buttonImageOnly ? '<img class="calendar_trigger" src="' + 
				this.buttonImage + '" alt="' + this.buttonText + '" title="' + this.buttonText + '"/>' :
				'<button class="calendar_trigger">' + (this.buttonImage != '' ? 
				'<img src="' + this.buttonImage + '" alt="' + this.buttonText + '" title="' + this.buttonText + '"/>' : 
				this.buttonText) + '</button>');
			$((this.buttonImageOnly ? 'img' : 'button') + '.calendar_trigger', $input.parent('span')).click(this.showFunction);
		}
		$input.keydown(this.keyDownFunction).keypress(this.keyPressFunction);
	},
	
	showCalendar: function() {
		this.popUpShowing = true;
		// build the calendar HTML
		html = (this.closeAtTop ? '<div id="calendar_control"><a id="calendar_clear">' + this.clearText + '</a>' +
			'<a id="calendar_close">' + this.closeText + '</a></div>' : '') +
			'<div id="calendar_links"><a id="calendar_prev">' + this.prevText + '</a>' +
			'<a id="calendar_current">' + this.currentText + '</a>' +
			'<a id="calendar_next">' + this.nextText + '</a></div>' +
			'<div id="calendar_header"><select id="calendar_newMonth">';
		inMinYear = (this.minDate != null && this.minDate.getFullYear() == this.selectedYear);
		inMaxYear = (this.maxDate != null && this.maxDate.getFullYear() == this.selectedYear);
		for (var month = 0; month < 12; month++) {
			if (!((inMinYear && month < this.minDate.getMonth()) ||
					(inMaxYear && month > this.maxDate.getMonth()))) {
				html += '<option value="' + month + '"' + 
					(month == this.selectedMonth ? ' selected="selected"' : '') + 
					'>' + this.getMonthName(month) + '</option>';
			}
		}
		html += '</select> <select id="calendar_newYear">';
		// determine range of years to display
		years = this.yearRange.split(':');
		if (years.length != 2) {
			year = this.selectedYear - 10;
			endYear = this.selectedYear + 10;
		}
		else if (years[0].charAt(0) == '+' || years[0].charAt(0) == '-') {
			year = this.selectedYear + parseInt(years[0]);
			endYear = this.selectedYear + parseInt(years[1]);
		}
		else {
			year = parseInt(years[0]);
			endYear = parseInt(years[1]);
		}
		if (this.minDate != null) {
			year = Math.max(year, this.minDate.getFullYear());
		}
		if (this.maxDate != null) {
			endYear = Math.min(endYear, this.maxDate.getFullYear());
		}
		for (; year <= endYear; year++) {
			html += '<option value="' + year + '"' + 
				(year == this.selectedYear ? ' selected="selected"' : '') + 
				'>' + year + '</option>';
		}
		html += '</select></div>' +
			'<table id="calendar" cellpadding="0" cellspacing="0"><thead>' +
			'<tr class="calendar_titleRow">';
		for (var dow = 0; dow < this.dayNames.length; dow++) {
			html += '<td>' + this.dayNames[(dow + this.firstDay) % 7] + '</td>';
		}
		html += '</tr></thead><tbody>';
		daysInMonth = this.getDaysInMonth(this.selectedYear, this.selectedMonth);
		this.selectedDay = Math.min(this.selectedDay, daysInMonth);
		noPrintDays = (this.getFirstDayOfMonth(this.selectedYear, this.selectedMonth) - this.firstDay + 7) % 7;
		currentDate = new Date(this.currentYear, this.currentMonth, this.currentDay);
		selectedDate = new Date(this.selectedYear, this.selectedMonth, this.selectedDay);
		printDate = new Date(this.selectedYear, this.selectedMonth, 1 - noPrintDays);
		numRows = Math.ceil((noPrintDays + daysInMonth) / 7); // calculate the number of rows to generate
		today = new Date();
		today = new Date(today.getFullYear(), today.getMonth(), today.getDate());
		for (var row = 0; row < numRows; row++) { // create calendar rows
			html += '<tr class="calendar_daysRow">';
			for (var dow = 0; dow < 7; dow++) { // create calendar days
				customSettings = (this.customDate == null ? [true, ''] : this.customDate(printDate));
				otherMonth = (printDate.getMonth() != this.selectedMonth);
				unselectable = otherMonth || !customSettings[0] || 
					(this.minDate != null && printDate < this.minDate) || 
					(this.maxDate != null && printDate > this.maxDate);
				html += '<td class="calendar_daysCell' + 
					((dow + this.firstDay + 6) % 7 >= 5 ? ' calendar_weekEndCell' : '') + // highlight weekends
					(otherMonth ? ' calendar_otherMonth' : '') + // highlight days from other months
					(printDate.getTime() == selectedDate.getTime() ? ' calendar_daysCellOver' : '') + // highlight selected day
					(unselectable ? ' calendar_unselectable' : '') +  // highlight unselectable days
					(!otherMonth || this.showOtherMonths ? ' ' + customSettings[1] : '') + '"' + // highlight custom dates
					(printDate.getTime() == currentDate.getTime() ? ' id="calendar_currentDay"' : // highlight current day
					(printDate.getTime() == today.getTime() ? ' id="calendar_today"' : '')) + '>' + // highlight today (if different)
					(otherMonth ? (this.showOtherMonths ? printDate.getDate() : '&nbsp;') : // display for other months
					(unselectable ? printDate.getDate() : '<a>' + printDate.getDate() + '</a>')) + '</td>'; // display for this month
				printDate.setDate(printDate.getDate() + 1);
			}
			html += '</tr>';
		}
		html += '</tbody></table><!--[if lte IE 6.5]><iframe src="javascript:false;" id="calendar_cover"></iframe><![endif]-->' +
			(this.closeAtTop ? '' : '<div id="calendar_control"><a id="calendar_clear">' + this.clearText + '</a>' +
			'<a id="calendar_close">' + this.closeText + '</a></div>');
		// add calendar to element to calendar Div
		$('#calendar_div').empty().append(html).show(this.speed);
		this.input[0].focus();
		this.setupDayLinks();
		// clear button link
		$('#calendar_clear').click(function() {
			popUpCal.clearDate();
		});
		// close button link
		$('#calendar_close').click(function() {
			popUpCal.hideCalendar(popUpCal.speed);
		});
		// setup navigation links
		$('#calendar_prev').click(function() {
			popUpCal.adjustDate(-1, 'M'); 
		});
		$('#calendar_next').click(function() {
			popUpCal.adjustDate(+1, 'M'); 
		});
		$('#calendar_current').click(function() {
			this.currentDay = new Date().getDate();
			popUpCal.selectedDay = new Date().getDate();
			popUpCal.selectedMonth = new Date().getMonth();
			popUpCal.selectedYear = new Date().getFullYear();
			popUpCal.showCalendar(); 
		});
		$('#calendar_newMonth').change(function() {
			popUpCal.selectedMonth = this.options[this.selectedIndex].value - 0;
			popUpCal.adjustDate(); 
		});
		$('#calendar_newYear').change(function() {
			popUpCal.selectedYear = this.options[this.selectedIndex].value - 0;
			popUpCal.adjustDate(); 
		});
	}, // end showCalendar
	
	setupDayLinks: function() {
		// set up link events on calendar table
		$('#calendar td[a]').hover( 
			function() {
				$(this).addClass('calendar_daysCellOver');
			}, function() {
				$(this).removeClass('calendar_daysCellOver');
		});
		$('#calendar a').click(function() {
			popUpCal.selectedDay = $(this).html();
			popUpCal.selectDate();
		});
	},
	
	hideCalendar: function(speed) {
		if (this.popUpShowing) {
			$('#calendar_div').hide(speed);
			this.popUpShowing = false;
			this.lastInput = null;
		}
	},
	
	selectDate: function() {
		this.hideCalendar(this.speed);
		setVal = this.formatDate(this.selectedDay, this.selectedMonth, this.selectedYear);
		this.input.val(setVal);		
	},

	clearDate: function() {
		this.hideCalendar(this.speed);
		this.input.val('');		
	},
	
	checkExternalClick: function(event) {
		if (popUpCal.popUpShowing) {
			node = event.target;
			cal = $('#calendar_div')[0];
			while (node != null && node != cal && node.className != 'calendar_trigger') {
				node = node.parentNode;
			}
			if (node == null) {
				popUpCal.hideCalendar();
			}
		}
	},
	
	noWeekends: function(date) {
		day = date.getDay();
		return [!(day == 0 || day == 6), ''];
	},
	
	/* Functions Dealing with Dates */
	formatDate: function(day, month, year) {
		month++; // adjust javascript month
		if (month <10) month = '0' + month; // add a zero if less than 10
		if (day < 10) day = '0' + day; // add a zero if less than 10
		var dateString = '';
		for (var i = 0; i < 3; i++) {
			dateString += this.dateFormat.charAt(3) + (this.dateFormat.charAt(i) == 'D' ? day : 
				(this.dateFormat.charAt(i) == 'M' ? month : 
				(this.dateFormat.charAt(i) == 'Y' ? year : '?')));
		}
		return dateString.substring(1);
	},
	
	setDateFromField: function() {
		currentDate = this.input.val().split(this.dateFormat.charAt(3));
		if (currentDate.length == 3) {
			this.currentDay = parseInt(this.trimNumber(currentDate[this.dateFormat.indexOf('D')]));
			this.currentMonth = parseInt(this.trimNumber(currentDate[this.dateFormat.indexOf('M')])) - 1;
			this.currentYear = parseInt(this.trimNumber(currentDate[this.dateFormat.indexOf('Y')]));
		} else {
			this.currentDay = new Date().getDate();
			this.currentMonth = new Date().getMonth();
			this.currentYear = new Date().getFullYear();
		}
		this.selectedDay = this.currentDay;
		this.selectedMonth = this.currentMonth;
		this.selectedYear = this.currentYear;
		this.adjustDate(0, 'D', true);
	},
	
	trimNumber: function(value) {
		if (value == '')
			return '';
		while (value.charAt(0) == '0') {
			value = value.substring(1);
		}
		return value;
	},
	
	adjustDate: function(offset, period, dontShow) {
		// adjust the data as requested
		if (period == 'D') {
			this.selectedDay = this.selectedDay + offset;
		}
		else if (period == 'M') {
			this.selectedMonth = this.selectedMonth + offset;
		}
		else if (period == 'Y') {
			this.selectedYear = this.selectedYear + offset;
		}
		date = new Date(this.selectedYear, this.selectedMonth, this.selectedDay);
		// ensure it is within the bounds set
		if (this.minDate != null) {
			date = (date > this.minDate ? date : this.minDate);
		}
		if (this.maxDate != null) {
			date = (date < this.maxDate ? date : this.maxDate);
		}
		this.selectedDay = date.getDate();
		this.selectedMonth = date.getMonth();
		this.selectedYear = date.getFullYear();
		if (!dontShow) {
			this.showCalendar();
		}
	},
	
	getMonthName: function(month) {
		return this.monthNames[month];
	},
	
	getDayName: function(day) {
		return this.dayNames[day];
	},
	
	getDaysInMonth: function(year, month) {
		return 32 - new Date(year, month, 32).getDate();
	},
	
	getFirstDayOfMonth: function(year, month) {
		return new Date(year, month, 1).getDay();
	},
	
	/* Position Functions */
	setPos: function(targetObj, moveObj) {
		var coords = this.findPos(targetObj);
		moveObj.css('position', 'absolute');
		moveObj.css('left', coords[0] + 'px');
		moveObj.css('top', (coords[1] + targetObj.offsetHeight) + 'px');
	},
	
	findPos: function(obj) {
		var curleft = curtop = 0;
		if (obj.offsetParent) {
			curleft = obj.offsetLeft;
			curtop = obj.offsetTop;
			while (obj = obj.offsetParent) {
				var origcurleft = curleft;
				curleft += obj.offsetLeft;
				if (curleft < 0) { 
					curleft = origcurleft;
				}
				curtop += obj.offsetTop;
			}
		}
		return [curleft,curtop];
	}
};

$.fn.calendar = function(settings) {
	// customise the calendar object
	if (settings) {
		for (var attr in settings) {
			popUpCal[attr] = settings[attr];
		}
	}
	// attach the calendar to each nominated input element
	this.each(function() {
		if (this.nodeName.toLowerCase() == 'input') {
			popUpCal.connectCalendar(this);
		}
	});
	return this;
};

// Initialise the calendar
$(document).ready(function() {
   popUpCal.init();
});
