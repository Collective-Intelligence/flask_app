# website_start

## Dev Tools

To avoid a lot of repetitive code and having to change variables by hand and
whatnot, I've opted to use Grunt to handle some automated tasks in `/styles` and
`/client`. To use this setup, follow these steps.

1. Install [Node.js](https://nodejs.org/en/)
1. Open a command line in the repository directory
1. Run `npm install` or `npm i`
1. Run `grunt watch`

For each subsequent use after all the installation, just run the last command.
Now you can edit the `.scss` and `.pug` files and Grunt will handle compiling
them into `.css` and `.html` files respectively upon saving.
