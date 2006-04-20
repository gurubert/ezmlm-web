<?cs def:checkbox(option)
	?><?cs if:Lang.Options[option]
		?><input type="checkbox" name="option_<?cs var:option ?>" id="option_<?cs
				var:option ?>" value="selected" <?cs
			if:(Data.List.Options[option] == 1) ?>checked="checked"<?cs
				/if ?> /> <label for="option_<?cs var:option ?>"><?cs
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
			if:(Data.List.Settings[setting].state == 1) ?>checked="checked"<?cs /if
				?> /> <label for="setting_state_<?cs var:setting ?>"><?cs
			var:html_escape(Lang.Settings[setting])
			?></label><ul><li><input type="text" name="setting_value_<?cs var:setting
			?>" id="setting_value_<?cs var:setting ?>" value="<?cs
			var:html_escape(Data.List.Settings[setting].value) ?>" size="30" /></li></ul>
		<input type="hidden" name="available_setting_<?cs
			var:setting ?>" value="true"><?cs
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
	?><?cs if:string.slice(text, index, index + string.length(search) - #1) == searchi
	?><?cs set:found = 1 ?><?cs /if
	?><?cs /loop ?><?cs
 /def ?><?cs

def:link(attr1, value1, attr2, value2, attr3, value3)
	?><?cs each:attrs = Temp
		?><?cs set:attrs = ""
	?><?cs /each
	?><?cs each:attrs = Config.UI.LinkAttrs
		?><?cs set:Temp[name(attrs)] = attrs
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
 /def ?>
