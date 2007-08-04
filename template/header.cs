<!DOCTYPE html
	PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	 "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html>

<head>
	<title><?cs var:Config.PageTitle ?></title>
	<meta http-equiv="pragma" content="no-cache" />	<!-- for browsers -->
	<meta http-equiv="cache-control" content="no-cache" />	<!-- for proxys -->
	<meta http-equiv="content-language" content="<?cs var:html_escape(Language) ?>" />
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<meta http-equiv="Author" content="devel[at]sumpfralle.de" />
	<meta http-equiv="expire" content="-1d" />
    <?cs each: item = Stylesheet
		?><link rel="stylesheet" type="text/css" href="<?cs var:item ?>" /><?cs
		/each ?>
</head>

<body>
	<table id="top"><tr>
		<td id="title">
			<h1>ezmlm-web</h1>
			<?cs if:Config.PageTitle
				?><p><?cs var:Config.PageTitle ?></p><?cs /if ?>
			</td>
		<td id="perm_nav">
			<?cs if:subcount(Config.PageLinks) > 0 ?><p><?cs
				loop: x = #0, subcount(Config.PageLinks)-1, #1
					?><?cs if:x > #0 ?> | <?cs /if
					?><a href="<?cs var:html_escape(Config.PageLinks[x].url)
						?>"><?cs var:html_escape(Config.PageLinks[x].name)
						?></a>
					<?cs /loop ?></p><?cs /if ?>
			<?cs if:UI.Top.Language || UI.Top.Interface ?>
				<?cs include: TemplateDir + '/interface_select.cs' ?>
			<?cs /if ?>
		</td>
	</tr></table>

