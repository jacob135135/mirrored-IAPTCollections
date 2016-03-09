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
	$('div').toggleClass("dyslexia");

	localStorage.setItem('dyslexia_on', "");
	if ($("body").hasClass("dyslexia"))
		localStorage.setItem('dyslexia_on', true);
}

function toggleContrast()
{
	$('.btn').toggleClass("high_contrast");
	$('input').toggleClass("high_contrast");
	$('textarea').toggleClass("high_contrast");
	$('body').toggleClass("high_contrast");
	$('#left_div').toggleClass("high_contrast");
	$('#right_div').toggleClass("high_contrast");
	$('#middle_div').toggleClass("high_contrast");
	$('#header_top').toggleClass("high_contrast");

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
	$('#sm_a').css('font-size', req_size - 2);
	$('#aa').css('font-size', req_size + 4);
  localStorage.setItem('font_req_size', req_size);
}

function deleteCollection(collection_id)
{
	ask=confirm("Are you sure you want to delete this collection? \n Items contained in this collection will be permanently lost");
    if(ask)
	{
		add_url = window.location.origin + "/IAPTCollections/default/delete_collection/" + collection_id;

		$.ajax({
		  url: add_url
		}).done(function() {
			window.location="/IAPTCollections/default/collections/";
		});
	}



}

function editCollection(item_id, list_id)
{
	{
		window.location="/IAPTCollections/default/edit_item/" + item_id + "?list_id=" + list_id;
	}
}

function initTrade()
{
		$( "#sortable1, #sortable2" ).sortable({
			connectWith: ".connectedSortable"
		}).disableSelection();

		$( "#sortable3, #sortable4" ).sortable({
			connectWith: ".connectedSortable2"
		}).disableSelection();
}

function runAdvSearchScripts()
{
	// When Only search collection of clicked
	$("#only_one_user").change(function() {
		if(this.checked) {
			$('#my_collection').attr('checked', false);
			$('#all_collections').attr('checked', false);

			$('#single_collection_owner').attr('disabled', false);

		}	else {
			$('#only_one_user').attr('checked', false);
			$('#single_collection_owner').attr('disabled', true);
		}
	});

	// When my_collection or all_collections checked
	$("#my_collection, #all_collections").change(function() {
		if(this.checked) {
			$('#only_one_user').attr('checked', false);
			$('#single_collection_owner').attr('disabled', true);
		}
	});

	// When untick all is checked
	$("#untickall").change(function() {
		if(this.checked) {
			$("#art,#music,#sports,#tech,#themed,#memorabilia,#ads,#architect,#books,#clothing,#coins,#glass,#house,#nature,#toys,#misc").attr('checked', false);

		}	else {
			$('#untickall').attr('checked', false);
		}
	});

	// When any of the categories checked
	$("#art,#music,#sports,#tech,#themed,#memorabilia,#ads,#architect,#books,#clothing,#coins,#glass,#house,#nature,#toys,#misc").change(function() {
		if(this.checked) {
			$('#untickall').attr('checked', false);
		}
	});
	triggerAutoComplUsers();
}

function getItemAllInfo(item_id, list_id)
{
	info_page = window.location.origin + "/IAPTCollections/default/item_info_by_id.json?id=" + item_id;

	$.ajax({
	  url: info_page
	}).done(function(data ) {
		if (!data['info'][0]['image'])
			img_src = "/IAPTCollections/static/images/question.jpg";
		else
			img_src = "/IAPTCollections/default/download/" + data['info'][0]['image'];

		list_name = '';
		if (list_id == 0)
		{
			list_name = "collection";
		}
		else if (list_id == 1)
		{
			list_name = "have list";
		}
		else if (list_id == 2)
		{
			list_name = "wish list";
		}

		del_url = window.location.origin + "/IAPTCollections/default/delete_item/" + list_id + "/" + data['info'][0]['id'];

		new_html = "<div class='item_view'><img src='" + img_src ;
		new_html += "' alt='selected item image' class='item_view_fit'></div>";
		new_html += "<div>Name: <b>" + data['info'][0]['name'] + "</b><br>";
		new_html += "<div>Value: <b>£" + data['info'][0]['price'] + "</b><br>";
		new_html += "<div>Owner: <b>" + data['owner'][0]['username'] + "</b><br>";
		new_html += "<div>Category: <b>" + data['info'][0]['type'] + "</b><br>";

		logged_in_id = data['logged_in'];
		owner_id = data['info'][0]['ownedBy'];


		new_html += "<label for='description'>Description:</label>";
		new_html += "<textarea class='form-control' id='description' rows='8' disabled>" + data['info'][0]['description'] + "</textarea>";
		item_id = data['info'][0]['id'];

		if (list_name)
		{
			new_html += "<button onclick='editCollection("+item_id+"," + list_id + ")' class='transp small_margins'><span class='glyphicon glyphicon-edit'></span>Edit item</button>";

			if (data['have_list_ok'] && list_id == 0)
				new_html += "<button onclick='addtoHavelist(" +item_id+ ")' class='transp small_margins'><span class='glyphicon glyphicon-plus'></span>Add to have list</button>";

			oncl =  "delItembyUrl('" + del_url + "')";

			new_html += "<button onclick=" + oncl + " class='transp small_margins'><span class='glyphicon glyphicon-trash'></span>Remove from " + list_name + "</button>";
		}
		else
		{
			if (data['wishlist_ok'])
				new_html += "<button onclick='addtoWishlist(" +item_id+ ")' class='transp small_margins'><span class='glyphicon glyphicon-plus'></span>Add to wishlist</button>";
		  if (data['is_tradable'])
				new_html += "<button onclick='proposeTrade(" + logged_in_id + "," + owner_id + ")' class='transp small_margins'><span class='glyphicon glyphicon-tags'></span>&nbsp;&nbsp;Propose trade</button>";
		}

		new_html += "</div>";

		$('#ajax_content_div').html(new_html);
	});
}

function addEnterListeners()
{
	$('#middle_div a').keydown( function(e) {
			var key = e.charCode ? e.charCode : e.keyCode ? e.keyCode : 0;
			if(key == 13) {
			 e.preventDefault();
				 $(this).click();
			}
	});
 }

function showLoginModal()
{
		$('#myModal').modal('show');
}

function redirIfAllowed(url)
{
	info_page = window.location.origin + "/IAPTCollections/default/logged_in.json"

	$.ajax({
	  url: info_page
	}).done(function(data ) {
		if (data['logged_in'] != null)
	{
		redir_url = window.location.origin + "/IAPTCollections/default/" + url;
		window.location.href = redir_url;
	}
	else
	{
		showLoginModal();
	}
	});
}

function redirToHome()
{
	window.location.href = window.location.origin + "/IAPTCollections/default/";
}

function delItembyUrl(url)
{
	$.ajax({
	  url: url
	}).done(function() {
		location.reload();
	});
}

function triggerAutoComplUsers()
{
	url = window.location.origin + "/IAPTCollections/default/all_users";
	$.ajax({
	  url: url
	}).done(function(data) {

		$("#single_collection_owner").autocomplete({
	      source: data
	    });
		});
}


function addtoHavelist(item_id)
{
	add_url = window.location.origin + "/IAPTCollections/default/add_item_to_havelist/" + item_id;

	$.ajax({
	  url: add_url
	}).done(function() {
		location.reload();
	});
}

function rejectTrade(trade_id)
{
	add_url = window.location.origin + "/IAPTCollections/default/delete_trade/" + trade_id;

	$.ajax({
	  url: add_url
	}).done(function() {
		window.location.href = window.location.origin + "/IAPTCollections/default/trade_history";
	});
}

function addtoWishlist(item_id)
{
	add_url = window.location.origin + "/IAPTCollections/default/add_item_to_wishlist/" + item_id;

	$.ajax({
	  url: add_url
	}).done(function() {
		location.reload();
	});
}

function proposeTrade(user1_id, user2_id, offer_id, editing)
{
	req_url = window.location.origin + "/IAPTCollections/default/trade/" + user1_id + "/" + user2_id;

	if(offer_id)
		req_url += "?show_offer=" +offer_id;

	if(editing)
		req_url += "?editing";
		window.location.href = req_url;
}


function proposeChosTrade(status, trade_id)
{
	pathname = window.location.pathname;
	user1_id = pathname.split("/")[4];
	user2_id = pathname.split("/")[5];

	user1_items = '';
	user2_items = '';

	$('#sortable3 li.clickable').each(function() {
  	user2_items += $(this).attr("data-id") + ",";
	});
	user2_items = user2_items.substr(0, user2_items.length -1);

	$('#sortable2 li').each(function() {
  	user1_items += $(this).attr("data-id") + ",";
	});
	user1_items = user1_items.substr(0, user1_items.length-1);


	// For some reason it is duplicated when it is populated from trade offer
	if (show_offer)
	{
		user1_items = user1_items.substr(0, user1_items.length/2);
		user2_items = user2_items.substr(0, user2_items.length/2);
	}

	if (user1_items && user2_items)
	{
		if (status == 'accept')
		{
			$.ajax({
				url: wwindow.location.origin + "/IAPTCollections/default/accept_trade/" + trade_id;
			}).done(function() {
				window.location.href = window.location.origin + "/IAPTCollections/default/trade_history";
			});
		}
		else
		{
			add_url = window.location.origin + "/IAPTCollections/default/create_new_trade";
		}

		$form = $("<form method='post' action=" + add_url +"></form>");
		$form.append("<input id='user_1_trading_items' name='user_1_trading_items' value=" + user1_items + ">");
		$form.append("<input id='user_2_trading_items' name='user_2_trading_items' value=" + user2_items + ">");
		$form.append("<input id='user_1' name='user_1' value=" + user1_id + ">");
		$form.append("<input id='user_2' name='user_2' value=" + user2_id + ">");
		$form.append("<input id='user_to_respond' name='user_to_respond' value=" + user2_id + ">");
		$('body').append($form);
		$form.submit();

		$.ajax({
		}).done(function() {
			window.location.href = window.location.origin + "/IAPTCollections/default/trade_history";
		});
	}
	else
	{
		$('.trading_div_errors').html("<b>Both users need to offer at least 1 item.</b>");
	}

}

function editTrade(trade_id)
{
	pathname = window.location.pathname;
	user1_id = pathname.split("/")[4];
	user2_id = pathname.split("/")[5];

	user1_items = '';
	user2_items = '';

	$('#sortable3 li.clickable').each(function() {
  	user2_items += $(this).attr("data-id") + ",";
	});
	user2_items = user2_items.substr(0, user2_items.length-3);

	$('#sortable2 li').each(function() {
  	user1_items += $(this).attr("data-id") + ",";
	});
	user1_items = user1_items.substr(0, user1_items.length-3);

	req_url = window.location.origin + "/IAPTCollections/default/edit_trade/" + trade_id;
	$form = $("<form method='post' action=" + req_url +"></form>");
	$form.append("<input id='user_1_trading_items' name='user_1_trading_items' value=" + user1_items + ">");
	$form.append("<input id='user_2_trading_items' name='user_2_trading_items' value=" + user2_items + ">");
	$form.append("<input id='user_1' name='user_1' value=" + user1_id + ">");
	$form.append("<input id='user_2' name='user_2' value=" + user2_id + ">");
	$form.append("<input id='user_to_respond' name='user_to_respond' value=" + user2_id + ">");
	$('body').append($form);
	$form.submit();

	$.ajax({
	}).done(function() {
		window.location.href = window.location.origin + "/IAPTCollections/default/trade_history";
	});
}


function initEnterSupp()
{
	$('#sortable1 li.clickable').keydown( function(e) {
			var key = e.charCode ? e.charCode : e.keyCode ? e.keyCode : 0;
			if(key == 13) {
			 e.preventDefault();
				 $('#sortable2').append(this);
				 $('#sortable1 li.clickable').focus();
				 initEnterSupp();
			}
	});

	$('#sortable2 li.clickable').keydown( function(e) {
			var key = e.charCode ? e.charCode : e.keyCode ? e.keyCode : 0;
			if(key == 13) {
			 e.preventDefault();
				 $('#sortable1').append(this);
				 $('#sortable2 li.clickable').focus();
				 initEnterSupp();
			}
	});

	$('#sortable4 li.clickable').keydown( function(e) {
			var key = e.charCode ? e.charCode : e.keyCode ? e.keyCode : 0;
			if(key == 13) {
			 e.preventDefault();
				 $('#sortable3').append(this);
				 $('#sortable4 li.clickable').focus();
				 initEnterSupp();
			}
	});

	$('#sortable3 li.clickable').keydown( function(e) {
			var key = e.charCode ? e.charCode : e.keyCode ? e.keyCode : 0;
			if(key == 13) {
			 e.preventDefault();
				 $('#sortable4').append(this);
				 $('#sortable3 li.clickable').focus();
				 initEnterSupp();
			}
	});
}

function initTradeStuff()
{
	// Amend trade to be as offer
	show_offer = window.location.href.split("?")[1];
	if (show_offer)
	{

		editing = window.location.href.split("?")[2];
		if (editing == 'editing')
		{
			console.log("editing");
			initTrade();
			initEnterSupp();
		}

		console.log("view only");
		trade_id = show_offer.split("=")[1];
		req_url = window.location.origin + "/IAPTCollections/default/trade_info.json/" + trade_id;

		$.ajax({
		  url: req_url
		}).done(function(data) {
			us1 = data['user_1_trading_items'];
			us1 = us1.substr(0, us1.length-1).split(",");

			us2 = data['user_2_trading_items'];
			us2 = us2.substr(0, us2.length-1).split(",");

			us1.forEach(function(entry) {
				corresp_li = $("li[data-id='" + entry + "']")[0];
				$('#sortable2').append(corresp_li);
				corresp_li = $("li[data-id='" + entry + "']")[1];
				$('#modal_trade_st #sortable2').append(corresp_li);

			});

			us2.forEach(function(entry) {
				corresp_li = $("li[data-id='" + entry + "']")[0];
				$('#sortable3').append(corresp_li);
				corresp_li = $("li[data-id='" + entry + "']")[1];
				$('#modal_trade_st #sortable3').append(corresp_li);
			});

			$('.propose_trade').after("<button onclick='rejectTrade("+ trade_id + ")' class='transp small_margins'><span class='glyphicon glyphicon-thumbs-down'></span>Reject trade</button>");

			if (editing != 'editing')
			{
				pathname = window.location.pathname;
				user1_id = pathname.split("/")[4];
				user2_id = pathname.split("/")[5];
				oncl = "proposeTrade(" + user1_id + "," + user2_id + "," + trade_id + ",'editing')";
				$('.propose_trade').after("<button onclick=" + oncl + " class='transp small_margins'><span class='glyphicon glyphicon-edit'></span>Edit trade</button>");

				$('.propose_trade').html("<span class='glyphicon glyphicon-thumbs-up'></span>Accept trade");
				$('.propose_trade').attr("onclick","proposeChosTrade('accept'," + trade_id +")");

			}
			else
			{
				$('.propose_trade').after("<button onclick='editTrade(" + trade_id + ")' class='transp small_margins'><span class='glyphicon glyphicon-shopping-cart'></span>Amend trade</button>");
				$('.propose_trade').remove();
			}


		});

	}
	else
	{
		initTrade();
		initEnterSupp();
	}

}
