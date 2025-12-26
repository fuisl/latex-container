# Use XeLaTeX as the default engine
$pdf_mode = 5;  # 5 = XeLaTeX

# Alternative: Use LuaLaTeX instead
# $pdf_mode = 4;  # 4 = LuaLaTeX

# Additional options
$biber = 'biber %O %S';
$bibtex_use = 2;  # Use biber instead of bibtex

# Maximum passes to prevent infinite loops
$max_repeat = 5;

# Show warnings but reduce verbosity
$silent = 0;

# Enable glossaries support - simplified version
add_cus_dep('glo', 'gls', 0, 'run_makeglossaries');
add_cus_dep('acn', 'acr', 0, 'run_makeglossaries');

sub run_makeglossaries {
    my $base = shift;
    system("makeglossaries '$base'");
}

# Ensure latexmk knows about glossary files
$clean_ext .= ' %R.ist %R.acn %R.acr %R.alg %R.glg %R.glo %R.gls';

# Preview settings - uncomment for continuous preview mode
# $preview_continuous_mode = 1;
# $pdf_previewer = 'start %O %S';
