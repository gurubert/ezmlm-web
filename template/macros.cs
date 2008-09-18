<?cs def:checkbox(option)
	?><?cs if:Lang.Options[option]
		?><input type="checkbox" name="option_<?cs var:option
				?>" id="option_<?cs var:option ?>" value="selected" <?cs
			if:(Data.List.Options[option] == 1) ?>checked="checked" <?cs
					/if ?>/>
				<label for="option_<?cs var:option ?>"><?cs
				var:html_escape(Lang.Options[option])
			?></label>
		<input type="hidden" name="available_option_<?cs
			var:option ?>" value="true" /><?cs
	else ?>unknown option (<?cs var:option ?>)<?cs /if ?><?cs
 /def ?><?cs

def:setting(setting)
	?><?cs if:Lang.Settings[setting]
		?><input type="checkbox" name="setting_state_<?cs var:setting
			?>" id="setting_state_<?cs var:setting ?>" value="selected" <?cs
			if:(Data.List.Settings[setting].state == 1) ?>checked="checked"<?cs
				/if ?> />
			<label for="setting_state_<?cs var:setting ?>"><?cs
			var:html_escape(Lang.Settings[setting])
			?></label><ul><li><input type="text" name="setting_value_<?cs var:setting
			?>" id="setting_value_<?cs var:setting ?>" value="<?cs
			var:html_escape(Data.List.Settings[setting].value) ?>" size="30" /></li></ul>
		<input type="hidden" name="available_setting_<?cs
			var:setting ?>" value="true" /><?cs
	else ?>unknown setting (<?cs var:setting ?>)<?cs /if ?><?cs
 /def ?><?cs

def:warning(warntext)
    ?><div class="warning"><?cs alt:html_escape(warntext) ?>unknown warning message (<?cs
			var:html_escape(Data.Warning) ?>)<?cs /alt ?></div><?cs
 /def ?><?cs

def:error(errtext)
    ?><div class="error">
		<?cs alt:html_escape(errtext) ?>unknown error message (<?cs
			var:html_escape(Data.Error) ?>)<?cs /alt ?></div><?cs
 /def ?><?cs

def:success(succtext)
    ?><div class="success">
		<?cs alt:html_escape(succtext) ?>unknown success message (<?cs 
		var:html_escape(Data.Success) ?>)<?cs /alt ?></div><?cs
 /def ?><?cs

def:limit_string_len(text,limit)
	?><?cs set:text2 = text ?><?cs set:len = string.length(text2) ?><?cs
	if:len > limit ?><?cs 
		var:string.slice(text,0,limit / #2 + limit % #2 - 1) ?>...<?cs
		var:string.slice(text,len - limit / #2 + #3 - #1, len) ?><?cs 
	else ?><?cs var:text ?><?cs /if ?><?cs
 /def ?><?cs

def:show_one_option(optname)
	?><?cs set:blacklist_found = 0 ?><?cs
		each:black_opt = Data.List.OptionsBlackList
			?><?cs if:black_opt == optname ?><?cs set:blacklist_found = 1 ?><?cs
			/if ?><?cs
		/each ?><?cs
	if:blacklist_found == 0 ?><?cs
		linclude:TemplateDir + '/config_options/' + optname + '.cs' ?><?cs
		/if ?><?cs
 /def ?><?cs

def:show_options(element)
	?><?cs if:subcount(element) == 0 ?><li><?cs
		call:show_one_option(element) ?></li><?cs
	else ?><?cs if:element["Self"] ?><li><?cs
			call:show_one_option(element["Self"]) ?><?cs
		/if ?><ul><?cs each:opts = element ?><?cs if:name(opts) != "Self" ?><?cs
			call:show_options(opts) ?><?cs
			/if ?><?cs /each
		?></ul><?cs if:element["Self"] ?></li><?cs /if ?><?cs
	/if ?><?cs
 /def ?><?cs


def:is_substring(text_in, search_in)
	?><?cs set:text = text_in
	?><?cs set:search = search_in
	?><?cs set:found = 0
	?><?cs loop: index = #0, string.length(text), #1
	?><?cs if:string.slice(text, index, index + string.length(search) - #1) == searchi
	?><?cs set:found = 1 ?><?cs /if
	?><?cs /loop ?><?cs
 /def ?><?cs

def:link(attr1, value1, attr2, value2, attr3, value3)
	?><?cs each:attrs = Temp
		?><?cs set:attrs = ""
	?><?cs /each
	?><?cs each:attrs = Config.UI.LinkAttrs
		?><?cs set:Temp[url_escape(name(attrs))] = url_escape(attrs)
		?><?cs /each
	?><?cs if:attr1 != "" ?><?cs set:Temp[attr1] = value1 ?><?cs /if
	?><?cs if:attr2 != "" ?><?cs set:Temp[attr2] = value2 ?><?cs /if
	?><?cs if:attr3 != "" ?><?cs set:Temp[attr3] = value3 ?><?cs /if
	?><?cs var:ScriptName
	?><?cs set:first_each = 1
	?><?cs if:subcount(Temp) > 0
		?><?cs each:attrs = Temp
			?><?cs if:(name(attrs) != "") && (attrs != "")
				?><?cs if:first_each == 1 ?><?cs
					set:first_each = 0 ?>?<?cs
				else
					?>&amp;<?cs /if
				?><?cs var:url_escape(name(attrs)) ?>=<?cs var:url_escape(attrs)
			?><?cs /if
		?><?cs /each
	?><?cs /if ?><?cs
 /def ?><?cs


def:form_header_generic(form_name, enctype, ignore1, ignore2, ignore3)
	?><?cs # somehow perl's CGI has problems to evaluate the querystring of a
		form action - thus we have to use hidden input fields instead
	?><form accept-charset="utf-8" name="<?cs var:html_escape(form_name)
			?>" method="post" action="<?cs var:ScriptName
			?>" enctype="<?cs var:enctype ?>">
		<?cs each:attr = Config.UI.LinkAttrs ?><?cs
			if:(name(attr) != ignore1) && (name(attr) != ignore2)
					&& (name(attr) != ignore3) ?><input type="hidden" name="<?cs
				var:html_escape(name(attr)) ?>" value="<?cs
				var:html_escape(attr) ?>" /><?cs /if ?>
		<?cs /each ?><?cs
		if:Data.List.Name ?><input type="hidden" name="list" value="<?cs
			var:html_escape(Data.List.Name) ?>" /><?cs /if ?><?cs
 /def ?><?cs


def:form_header(form_name)
	?><?cs call:form_header_generic(form_name,
			"application/x-www-form-urlencoded", '', '', '') ?><?cs
 /def ?><?cs


def:form_header_ignore(form_name, ignore1, ignore2, ignore3)
	?><?cs call:form_header_generic(form_name,
			"application/x-www-form-urlencoded", ignore1, ignore2, ignore3)
 ?><?cs /def ?><?cs


def:form_header_upload(form_name)
	?><?cs call:form_header_generic(form_name, "multipart/form-data",
			'', '', '') ?><?cs
 /def ?><?cs


def:check_active_selection(input)
	?><?cs set:selection=input
	?><?cs set:match_ok = 1 ?><?cs
	set:slen = string.length(selection) ?><?cs
	loop: sindex = #0, slen-1, #1 ?><?cs
		set:selection_char = string.slice(selection, sindex, sindex+1) ?><?cs
		if:(Data.List.Options[selection_char] != "1") ?><?cs
			set:match_ok = 0 ?><?cs /if ?><?cs
	/loop ?><?cs if:match_ok == 1 ?> checked="checked" <?cs /if ?><?cs
 /def ?><?cs


def:selection_list(sel_name)
	?><?cs var:html_escape(Lang.Selections[sel_name])
	?>:<br/>
	<ul><?cs each:item = Lang.Selections[sel_name] ?>
			<li><input type="radio" name="selection_<?cs var:sel_name
				?>" value="<?cs var:name(item) ?>" id="selection_<?cs
				var:sel_name + '_' + name(item) ?>" <?cs
				call:check_active_selection(name(item)) ?> />
				<label for="selection_<?csvar:sel_name + '_' + name(item)
				?>"><?cs var:html_escape(item) ?></label></li><?cs /each ?>
	</ul>
 <?cs /def ?><?cs


def:selection_checkboxes(sel_name)
	?><?cs var:html_escape(Lang.Selections[sel_name]) ?>:
	<ul><?cs each:item = Lang.Selections[sel_name] ?>
		<li><input type="checkbox" value="enabled" name="option_<?cs
				var:name(item) ?>" id="selection_<?cs
				var:sel_name + '_' + name(item) ?>" <?cs
				call:check_active_selection(name(item)) ?> />
				<input type="hidden" name="available_option_<?cs
				var:name(item) ?>" value="enabled" />
				<label for="selection_<?cs var:sel_name + '_' + name(item)
				?>"><?cs var:html_escape(item) ?></label></li>
		<?cs /each ?>
	</ul>
 <?cs /def ?>

