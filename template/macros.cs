<?cs def:checkbox(option)
	?><?cs if:Lang.Options[option]
		?><input type="checkbox" name="option_<?cs var:option ?>" id="option_<?cs
				var:option ?>" value="selected" <?cs
			if:(Data.List.Options[option] == 1) ?>checked="checked"<?cs
				/if ?> /> <label for="option_<?cs var:option ?>"><?cs
				var:html_escape(Lang.Options[option])
			?></label><?cs
		set:available_options = available_options + option ?><?cs
	else ?>unknown option (<?cs var:option ?>)<?cs /if ?><?cs
 /def ?><?cs

def:setting(setting)
	?><?cs if:Lang.Settings[setting]
		?><input type="checkbox" name="setting_state_<?cs var:setting
			?>" id="setting_state_<?cs var:setting ?>" value="selected" <?cs
			if:(Data.List.Settings[setting].state == 1) ?>checked="checked"<?cs /if
				?> /> <label for="setting_state_<?cs var:setting ?>"><?cs
			var:html_escape(Lang.Settings[setting])
			?></label><ul><li><input type="text" name="setting_value_<?cs var:setting
			?>" id="setting_value_<?cs var:setting ?>" value="<?cs
			var:html_escape(Data.List.Settings[setting].value) ?>" size="30" /></li></ul><?cs
		set:available_settings = available_settings + setting ?><?cs
	else ?>unknown setting (<?cs var:setting ?>)<?cs /if ?><?cs
 /def ?><?cs

def:warning(warntext)
    ?><div class="warning"><?cs alt:warntext ?>unknown warning message (<?cs
			var:Data.Warning ?>)<?cs /alt ?></div><?cs
 /def ?><?cs

def:error(errtext)
    ?><div class="error">
		<?cs alt:errtext ?>unknown error message (<?cs
			var:Data.Error ?>)<?cs /alt ?></div><?cs
 /def ?><?cs

def:success(succtext)
    ?><div class="success">
		<?cs alt:succtext ?>unknown success message (<?cs 
		var:Data.Success ?>)<?cs /alt ?></div><?cs
 /def ?><?cs

def:limit_string_len(text,limit)
	?><?cs set:text2 = text ?><?cs set:len = string.length(text2) ?><?cs
	if:len > limit ?><?cs 
		var:string.slice(text,0,limit / #2 + limit % #2 - 1) ?>...<?cs
		var:string.slice(text,len - limit / #2 + #3 - #1, len) ?><?cs 
	else ?><?cs var:text ?><?cs /if ?><?cs
 /def ?><?cs

def:show_options(element)
	?><?cs if:subcount(element) == 0 ?><li><?cs
		linclude:TemplateDir + '/config_options/' + element + '.cs' ?></li><?cs
	else ?><?cs if:element["Self"] ?><li><?cs
			linclude:TemplateDir + '/config_options/' + element["Self"] + '.cs' ?><?cs
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
	?><?cs if:string.slice(text, index, index + string.length(search) - #1) == search ?><?cs set:found = 1 ?><?cs /if
	?><?cs /loop ?><?cs
 /def ?>
