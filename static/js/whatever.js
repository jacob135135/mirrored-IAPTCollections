function doStuffOnload()
{
	if (isFontSizeDefined())
	{
		req_size = parseInt(localStorage.getItem('font_req_size'));
		applySizing(req_size);
	}

	if (localStorage.getItem('dyslexia_on'))
	{
		toggleDyslexia();
	}

	if (localStorage.getItem('high_contrast_on'))
	{
		toggleContrast();
	}
}

function toggleDyslexia()
{
	$('.btn').toggleClass("dyslexia");
	$('body').toggleClass("dyslexia");

	localStorage.setItem('dyslexia_on', "");
	if ($("body").hasClass("dyslexia"))
		localStorage.setItem('dyslexia_on', true);
}

function toggleContrast()
{
	$('.btn').toggleClass("high_contrast");
	$('body').toggleClass("high_contrast");

	localStorage.setItem('high_contrast_on', "");
	if ($("body").hasClass("high_contrast"))
		localStorage.setItem('high_contrast_on', true);
}

function incFont()
{
	current_size = $('body').css('font-size');
	if (isFontSizeDefined())
		current_size = parseInt(localStorage.getItem('font_req_size'))

	req_size = parseInt(current_size) + 2;
	applySizing(req_size);
}

function decFont()
{
	current_size = $('body').css('font-size');
	if (isFontSizeDefined())
		current_size = parseInt(localStorage.getItem('font_req_size'))

	req_size = parseInt(current_size) - 2;
  applySizing(req_size);
}

function isFontSizeDefined()
{
	if (typeof localStorage.getItem('font_req_size') !== 'undefined')
		return true;
}

function applySizing(req_size)
{
  $('body').css('font-size', req_size);
  $('.btn').css('font-size', req_size);
  $('input').css('font-size', req_size);
  localStorage.setItem('font_req_size', req_size);
}
